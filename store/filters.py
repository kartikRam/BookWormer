import django_filters
from django_filters import DateFilter,CharFilter
from .models import *

class BookFilter(django_filters.FilterSet):

    name=CharFilter(field_name="name",lookup_expr='icontains')
    class Meta:
        model=books
        fields='__all__'
        exclude=['description','isbn','image','price']
