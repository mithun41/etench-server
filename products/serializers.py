from rest_framework import serializers
from products.models import Product, Category

# Public / Admin একি serializer ব্যবহার করা যাবে
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'stock', 'image',
            'commission_rate', 'created_at', 'updated_at', 'category', 'category_id'
        ]
