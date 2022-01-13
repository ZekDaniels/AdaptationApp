from adaptation.api.serializers import *
from django.core.validators import EMPTY_VALUES
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework_datatables.filters import DatatablesFilterBackend

from adaptation.models import Faculty

class QueryListAPIView(generics.ListAPIView):
    def get_queryset(self):
        if self.request.GET.get('format', None) == 'datatables':
            self.filter_backends = (OrderingFilter, DatatablesFilterBackend)
            return super().get_queryset()
        queryset = self.queryset

        # check the start index is integer
        try:
            start = self.request.GET.get('start')
            start = int(start) if start else None
        # else make it None
        except ValueError:
            start = None

        # check the end index is integer
        try:
            end = self.request.GET.get('end')
            end = int(end) if end else None
        # else make it None
        except ValueError:
            end = None

        # skip filters and sorting if they are not exists in the model to ensure security
        accepted_filters = {}
        # loop fields of the model
        for field in queryset.model._meta.get_fields():
            # if field exists in request, accept it
            if field.name in dict(self.request.GET):
                accepted_filters[field.name] = dict(self.request.GET)[field.name]
            # if field exists in sorting parameter's value, accept it

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
            queryset = queryset.all().filter(**filters)[start:end]
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

class AdaptationCreateAPIView(generics.CreateAPIView):
   
    queryset = Adaptation.objects.all()
    serializer_class = AdaptationCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdaptationUpdateAPIView(generics.UpdateAPIView):
   
    queryset = Adaptation.objects.all()   
    serializer_class = AdaptationCreateSerializer
    
class StudentClassListAPIView(QueryListAPIView):
   
    custom_related_fields = ["adaptation_class","adaptation"]
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
        return super().destroy(request, *args, **kwargs)
