import django_filters
from django_filters import rest_framework as filters

from core.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    is_published = django_filters.BooleanFilter(field_name='is_published')
    class Meta:
        model = Product
        fields = {
            'price': ['lte', 'gte'],
            'name': ['icontains',],
            'categories': ['exact',]
        }