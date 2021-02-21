from django.shortcuts import render
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.filters import ProductFilter
from core.models import Product, Category
from core.serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ]
    queryset = Product.objects.filter(is_deleted=False)
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['name', 'categories']
    filterset_class = ProductFilter

    @action(methods=['GET'], detail=False, url_path="deleted", url_name="deleted", filter_backends=[])
    def deleted(self, request):
        queryset = Product.objects.filter(is_deleted=True)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      ):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]
    queryset = Category.objects.all()


class ProductsByCategory(ListView):
    model = Product

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Product.objects.filter(is_deleted=False, type=slug)

class PBCViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny,]
    lookup_field = 'category'
    lookup_value_regex = '[\w-]+'

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False, categories=self.kwargs['category'])
