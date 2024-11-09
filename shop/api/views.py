from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from shop.models import Clothes, Rental
from .serializers import Clothserializer, Rentalserializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .filters import ClotheFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class HomeListAPIView(ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ClotheFilter
    serializer_class = Clothserializer
    search_fields = ['name', 'description']
    queryset = Clothes.objects.all() 


class DetailAPIView(APIView):
    def get(self, request, cloth_id):
        cloth = Clothes.objects.get(id=cloth_id)
        serializer = Clothserializer(cloth)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, cloth_id):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        duration = request.data.get("duration")
        rental_date = request.data.get("rental_date", timezone.now())

        try:
            clothe = Clothes.objects.get(id=cloth_id)
            user_id = request.user.id
            price_per_day = clothe.price
            total_price = int(duration) * price_per_day  # Calculate the total price
              # Fetch the Clothes instance
        except Clothes.DoesNotExist:
            return Response(
                {"error": "Clothes not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if isinstance(rental_date, timezone.datetime):
            rental_date = rental_date.date()  # Convert to date
        rental_data = {
            "clothe": clothe,
            "user": user_id,
            "rental_date": rental_date,
            "duration": duration,
            "total_price": total_price,
            # Add other required fields for Rental serializer if necessary
        }
        
        serializer = Rentalserializer(data = rental_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RentedAPIView(APIView):
    def get(self, request):
        user = user.request
        queryset = Clothes.objects.filter(user=user)
        serializer = Clothserializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
