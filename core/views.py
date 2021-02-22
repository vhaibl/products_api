from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, mixins, status
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
    filterset_class = ProductFilter

    @action(methods=['GET'], detail=False, url_path="deleted", url_name="deleted", filter_backends=[])
    def deleted(self, request):
        queryset = Product.objects.filter(is_deleted=True)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      ):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]
    queryset = Category.objects.all()
    lookup_field = 'type'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except ValueError as er:
            return Response({'error': f'{er}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PBCViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ]
    lookup_field = 'category'
    lookup_value_regex = '[\w-]+'

    def get_queryset(self):
        try:
            categories = Category.objects.filter(type__icontains=self.kwargs['category'])
        except Exception as er:
            raise ValueError({'error': f'{er}'})
        suitable = []
        for category in categories:
            suitable += Product.objects.filter(is_deleted=False, categories=category.id)
        return suitable
