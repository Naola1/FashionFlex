from rest_framework import serializers
from shop.models import Clothes, Rental, Category


class CategorySerializer(serializers.ModelSerializer):
    # Recursive relationship to get parent categories
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']

    def get_parent(self, obj):
        if obj.parent is not None:
            return CategorySerializer(obj.parent).data
        return None


class Clothserializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Clothes
        fields = [
            'name', 'size', 'color', 'price', 'description', 'availability', 
            'rating', 'stock', 'condition', 'views_count', 'created_at', 
            'updated_at', 'category'
        ]


class Rentalserializer(serializers.ModelSerializer):
    clothe = serializers.SlugRelatedField(queryset=Clothes.objects.all(), slug_field='name', required=False)
    class Meta:
        model = Rental
        fields = [
            'clothe', 'user', 'rental_date', 'duration', 'total_price', 
            'created_at', 'updated_at'
        ]
