# cart/api/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart, CartItem
from shop.models import Clothes
from .serializers import CartSerializer, CartItemSerializer

class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, clothes_id):
        try:
            clothes = Clothes.objects.get(id=clothes_id)
        except Clothes.DoesNotExist:
            return Response({"detail": "Clothes item not found"}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, Clothes=clothes)

        if not created:
            cart_item.quantity += 1  # Increase quantity if already exists
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, clothes_id):
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.filter(cart=cart, Clothes_id=clothes_id).first()
        
        if cart_item:
            cart_item.delete()
            return Response({"detail": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)
