from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from clothes.models import Clothes, Rental
from .serializers import Clothserializer, Rentalserializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

class HomeListAPIView(ListAPIView):
    serializer_class = Clothserializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if query:
            return Clothes.objects.filter(category=query)  
        return Clothes.objects.all()

class DetailAPIView(APIView):
    def get(self, request):
        cloth_id = request.GET.get('id')
        cloth = Clothes.objects.get(id=cloth_id)
        serializer = Clothserializer(cloth)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DetailAPIView(APIView):
    def post(self, request):
        clothe_id = request.POST.get('id')
        print(clothe_id)
        duration = request.POST.get('duration')
        rental_date = request.POST.get('rental_date', timezone.now())

        try:
            clothe = Clothes.objects.get(id=clothe_id)  # Fetch the Clothes instance
        except Clothes.DoesNotExist:
            return Response({'error': 'Clothes not found.'}, status=status.HTTP_404_NOT_FOUND)

        rental = Rental(
            clothe=clothe,
            rental_date=rental_date,
            duration=duration,
        )

        serializer = Rentalserializer(rental)
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
