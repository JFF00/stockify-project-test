from rest_framework import serializers
from .models import Category, Product, Movement, Record



class CategorySerializer(serializers.ModelSerializer):
    id_category = serializers.IntegerField(read_only=True)
    created_at = serializers.DateField(read_only=True)
    class Meta:
        model = Category
        fields = ['id_category', 'name', 'description', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    id_product = serializers.IntegerField(read_only=True)
    created_at = serializers.DateField(read_only=True)
    id_category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Product
        fields = ['id_product', 'name', 'description', 'stock', 'unit_price', 'created_at', 'id_category']

class RecordSerializer(serializers.ModelSerializer):
    id_movement = serializers.PrimaryKeyRelatedField(read_only=True)
    id_product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Record
        fields = ['id_movement', 'id_product', 'amount']

class MovementSerializer(serializers.ModelSerializer):
    id_movement = RecordSerializer(source= 'ecord_set', many=True, read_only=True)
    id_user = serializers.PrimaryKeyRelatedField(read_only=True)
    records = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Movement
        fields = ['id_movement', 'id_user', 'date', 'type', 'records']

