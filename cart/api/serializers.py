# cart/api/serializers.py
from rest_framework import serializers
from cart.models import Cart, CartItem
from shop.models import Clothes  # Import Clothes model

class CartItemSerializer(serializers.ModelSerializer):
    clothes_name = serializers.ReadOnlyField(source='Clothes.name')  # Optional: adds clothes name to the response
    total_price = serializers.SerializerMethodField()  # Custom field for total price

    class Meta:
        model = CartItem
        fields = ['id', 'Clothes', 'clothes_name', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()  # Calls get_total_price from the model

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Nested serializer for cart items

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']
        read_only_fields = ['user', 'created_at']
