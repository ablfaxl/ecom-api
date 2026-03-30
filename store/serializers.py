from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'parent']
class ProductSerializer(serializers.ModelSerializer):
    # مقدار صحیح read_only=True است
    category = CategorySerializer(read_only=True) 
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'inventory', 'category', 'image']