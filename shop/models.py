from django.db import models
from django.utils import timezone
from datetime import timedelta


class Clothes(models.Model):
    CATEGORY_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("children", "Children"),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Price per day with decimals
    description = models.TextField()
    image = models.ImageField(upload_to="clothes/")
    rating = models.IntegerField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    stock = models.IntegerField()

    def __str__(self):
        return self.name


class Rental(models.Model):
    DURATION_CHOICES = [
        (2, "2 days"),
        (4, "4 days"),
        (8, "8 days"),
    ]

    clothe = models.ForeignKey(
        Clothes, on_delete=models.CASCADE, related_name="rentals"
    )
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Uncomment if user authentication is implemented
    rental_date = models.DateField(
        default=timezone.now
    )  # Date the user wants the cloth
    duration = models.IntegerField(choices=DURATION_CHOICES)  # Duration in days
    return_date = models.DateField(blank=True, null=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    def calculate_total_price(self):
        return self.clothe.price * self.duration

    def calculate_return_date(self):
        return self.rental_date + timedelta(days=self.duration)

    def save(self, *args, **kwargs):
        # Automatically calculate the total price and return date before saving
        self.total_price = self.calculate_total_price()
        self.return_date = self.calculate_return_date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rental of {self.clothe.name} for {self.duration} days"
