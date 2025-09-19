from rest_framework import serializers
from .models import Category, Product



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    id_product = serializers.IntegerField(read_only=True)
    created_at = serializers.DateField(read_only=True)
    id_category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Product
        fields = ['id_product', 'name', 'description', 'stock', 'unit_price', 'created_at', 'id_category']