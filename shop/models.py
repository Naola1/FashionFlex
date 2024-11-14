from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import User
from django.utils.text import slugify

# Category Model with unique slug
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
# Clothes Model
class Clothes(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='clothes')
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="clothes/")
    availability = models.BooleanField(default=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Rating from 1 to 5
    stock = models.PositiveIntegerField()
    condition = models.CharField(max_length=50, default="new")
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Rental Model
class Rental(models.Model):
    DURATION_CHOICES = [
        (2, "2 days"),
        (4, "4 days"),
        (8, "8 days"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("returned", "Returned"),
        ("overdue", "Overdue"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rentals")
    clothe = models.ForeignKey(Clothes, on_delete=models.CASCADE, related_name="rentals")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    rental_date = models.DateField(default=timezone.now)
    duration = models.IntegerField(choices=DURATION_CHOICES)
    return_date = models.DateField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_extended = models.BooleanField(default=False)
    extended_return_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        return self.clothe.price * self.duration

    def calculate_return_date(self):
        return self.rental_date + timedelta(days=self.duration)

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        if not self.return_date:
            self.return_date = self.calculate_return_date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rental of {self.clothe.name} for {self.duration} days"
