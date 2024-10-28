from rest_framework.serializers import ModelSerializer
from clothes.models import Clothes


class Clothserializer(ModelSerializer):
    class Meta:
        model = Clothes
        fields = ['id', 'name', 'description', 'price'] 

class Rentalserializer(ModelSerializer):
    class Meta:
        model = Clothes
        fields = ['clothe', 'rental_date', 'duration', 'return_date', 'total_price']