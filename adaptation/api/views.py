from adaptation.api.serializers import *
from django.core.validators import EMPTY_VALUES
from django.db.models import QuerySet, ForeignObjectRel, ForeignKey, Q
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_datatables.filters import DatatablesFilterBackend, f_search_q
from rest_framework.permissions import BasePermission

from adaptation.models import Faculty
from user.models import Profile

class AdminsPermissions(BasePermission):
    allowed_user_roles = (Profile.admin, Profile.commission_member, Profile.commission_lead)

    def has_permission(self, request, view):
        is_allowed_user = request.user.profile.user_role in self.allowed_user_roles
        return is_allowed_user

class CustomDatatablesFilterBackend(DatatablesFilterBackend):

    def get_q(self, datatables_query):
        q = Q()
        initial_q = Q()
        for f in datatables_query['fields']:
            if not f['searchable']:
                continue
            q |= f_search_q(f,
                            datatables_query['search_value'],
                            datatables_query['search_regex'])
            initial_q &= f_search_q(f,
                                    f.get('search_value'),
                                    f.get('search_regex', False))
        q &= initial_q
        return q

class QueryListAPIView(generics.ListAPIView):
    def get_queryset(self):
        if self.request.GET.get('format', None) == 'datatables':
            self.filter_backends = (OrderingFilter, CustomDatatablesFilterBackend)
            return super().get_queryset()
        queryset = self.queryset
        # skip filters and sorting if they are not exists in the model to ensure security
        accepted_filters = {}
        # loop fields of the model
        for field in queryset.model._meta.get_fields():
            # if field exists in request, accept it
            if field.name in dict(self.request.GET):
                accepted_filters[field.name] = dict(self.request.GET)[field.name]
            if isinstance(field, ForeignObjectRel) or isinstance(field, ForeignKey):
                for n in field.related_model._meta.get_fields():
                    related_field = f"{field.name}__{n.name}"
                    if related_field in dict(self.request.GET):
                        accepted_filters[related_field] = dict(self.request.GET)[related_field]
                        dict(self.request.GET)
        filters = {}
        for key, value in accepted_filters.items():
            if any(val in value for val in EMPTY_VALUES):
                if queryset.model._meta.get_field(key).null:
                    filters[key + '__isnull'] = True
                else:
                    filters[key + '__exact'] = ''
            else:
                filters[key + '__in'] = value
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.filter(**filters)
        return queryset

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            elif self.request.GET.get('format', None) == 'datatables':
                self._paginator = self.pagination_class()
            else:
                self._paginator = None
        return self._paginator


class UniversityListView(QueryListAPIView):
    
    queryset = University.objects.all()
    serializer_class = UniversityListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'

class FacultyListView(QueryListAPIView):
    
    custom_related_fields = ["university"]
    queryset = Faculty.objects.select_related(*custom_related_fields).all()
    serializer_class = FacultyListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'

class ScienceListView(QueryListAPIView):
    
    custom_related_fields = ["university"]
    queryset = Science.objects.select_related(*custom_related_fields).all()
    serializer_class = ScienceListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'

class AdaptationListView(QueryListAPIView):

    permission_classes = [AdminsPermissions, ]
    custom_related_fields = ["user"]
    queryset = Adaptation.objects.select_related(*custom_related_fields).all()
    serializer_class = AdaptationListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'

class AdaptationCreateAPIView(generics.CreateAPIView):
   
    queryset = Adaptation.objects.all()
    serializer_class = AdaptationCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdaptationUpdateAPIView(generics.UpdateAPIView):
       
    queryset = Adaptation.objects.all()   
    serializer_class = AdaptationCreateSerializer

class AdaptationAdminUpdateAPIView(generics.UpdateAPIView):
       
    permission_classes = [AdminsPermissions, ]
    queryset = Adaptation.objects.all()   
    serializer_class = AdaptationAdminUpdateSerializer

class AdaptationClassListAPIView(QueryListAPIView):

    queryset = AdapatationClass.objects.all()
    serializer_class = AdaptationClassListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'

class AdaptationClassDetailAPIView(generics.RetrieveAPIView):

    queryset = AdapatationClass.objects.all() 
    serializer_class = AdaptationClassListSerializer
    
class StudentClassListAPIView(QueryListAPIView):
   
    custom_related_fields = ["adaptation", "adaptation_class"]
    queryset = StudentClass.objects.select_related(*custom_related_fields).all().order_by('-adaptation_class__pk') 
    serializer_class = StudentClassListSerializer
    filter_backends = [OrderingFilter, SearchFilter]

    ordering_fields = "__all__"
    search_fields = ['code', 'class_name','adaptation_class__code', 'adaptation_class__class_name']


class StudentClassCreateAPI(generics.CreateAPIView):
    
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassCreateSerializer

class StudentClassUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassCreateSerializer

    def destroy(self, request, *args, **kwargs):

        
        instance = self.get_object()
        if not request.user.profile.is_allowed_user():
            if instance.adaptation.is_closed:
                raise serializers.ValidationError(("Bu intibak başvurusu kapatılmış, değiştirmek istediğinize eminseniz tekrar hocanıza başvurun."))
            
            if instance.adaptation.user != request.user:
                raise serializers.ValidationError(("Bu kullanıcının intibak başvurusunu değiştiremezsiniz."))
        with transaction.atomic(): 
            try:
                confirmation = instance.adaptation.confirmations.get(adaptation_class=instance.adaptation_class)  
            except:
                confirmation = None
            if confirmation:
                instance.adaptation.confirmations.get(adaptation_class=instance.adaptation_class).delete()
            return super().destroy(request, *args, **kwargs)

class AdaptationClosedUpdateAPIView(generics.UpdateAPIView):
    
    permission_classes = [AdminsPermissions, ]
    queryset = Adaptation.objects.all()
    serializer_class = AdaptationClosedUpdateSerializer


class AdaptationClassConfirmationCreateAPIView(generics.CreateAPIView):
    
    permission_classes = [AdminsPermissions, ]
    queryset = AdaptationClassConfirmation.objects.all()
    serializer_class = AdaptationClassConfirmationCreateSerializer

class AdaptationClassConfirmationDestroyAPIView(generics.DestroyAPIView):
    
    permission_classes = [AdminsPermissions, ]
    queryset = AdaptationClassConfirmation.objects.all()
    serializer_class = AdaptationClassConfirmationCreateSerializer