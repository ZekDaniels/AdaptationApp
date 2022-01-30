from adaptation.api.serializers import *
from django.core.validators import EMPTY_VALUES
from django.db.models import QuerySet, ForeignObjectRel, ForeignKey, Q
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_datatables.filters import DatatablesFilterBackend, f_search_q
from django.contrib.auth.models import User

from user.api.serializers import UserListSerializer


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


class UserListView(QueryListAPIView):

    # custom_related_fields = [""]
    # queryset = User.objects.select_related(*custom_related_fields).all()
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'
