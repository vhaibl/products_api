from rest_framework import serializers

from core.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('is_deleted',)

    def validate_categories(self, data):
        if len(data) not in range(2,10):
            raise serializers.ValidationError('Must be from 2 to 10 categories')
        return data


