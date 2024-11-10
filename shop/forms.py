# forms.py
from django import forms
from shop.models import Rental
from django.utils import timezone

class RentalForm(forms.ModelForm):
    duration = forms.IntegerField(min_value=1, label="Rental Duration (days)")
    rental_date = forms.DateField(initial=timezone.now().date(), widget=forms.SelectDateWidget)

    class Meta:
        model = Rental
        fields = ['duration', 'rental_date']
