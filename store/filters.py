import django_filters
from django_filters import DateFilter,CharFilter
from .models import *
from django import forms


class BookFilter(django_filters.FilterSet):

    name=CharFilter(field_name="name",lookup_expr='icontains')
    class Meta:
        model=books
        fields='__all__'
        exclude=['description','isbn','image','price']

class OrderFilter(django_filters.FilterSet):

    name = django_filters.ModelChoiceFilter(
        queryset=author.objects.all(),
        empty_label="All books",
        widget=forms.Select(attrs={'class': 'form-control'}),
        )

    class Meta:
        model=order
        fields='__all__'
        exclude=['user','quantity','price','date_created']
