from django.db import models
from django.utils import timezone
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    # Check if a category has no children
    def is_leaf(self):
        return not self.children.exists()

class Clothes(models.Model):
    GENDER_CHOICES = [
        ("women", "Women"),
        ("men", "Men"),
        ("children", "Children"),
    ]

    STYLE_CHOICES = [
        ("modern", "Modern (Western)"),
        ("traditional", "Traditional (Local)"),
    ]

    ETHNICITY_CHOICES = [
        ("oromo", "Oromo"),
        ("amhara", "Amhara"),
        ("tigray", "Tigray"),
        ("afar", "Afar"),
        ("snnpr", "SNNP"),
        ("somali", "Somali"),
        ("gambella", "Gambella"),
        ("harari", "Harari"),
    ]

    ITEM_TYPE_CHOICES = [
        ("clothing", "Traditional Clothing"),
        ("footwear", "Traditional Footwear"),
        ("accessories", "Traditional Accessories"),
    ]

    OCCASION_CHOICES = [
        ("casual", "Casual"),
        ("formal", "Formal"),
        ("activewear", "Activewear"),
        ("special", "Special Occasion"),
        ("sustainable", "Sustainable Fashion"),
    ]

    # Main fields for Clothes
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="clothes/")
    availability = models.BooleanField(default=True)
    rating = models.IntegerField()
    stock = models.PositiveIntegerField()
    condition = models.CharField(max_length=50, default="new")
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Foreign Key to Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='clothes')

    # Category fields
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    style = models.CharField(max_length=20, choices=STYLE_CHOICES)
    ethnicity = models.CharField(max_length=20, choices=ETHNICITY_CHOICES, blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, blank=True, null=True)
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name

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

    clothe = models.ForeignKey(
        Clothes, on_delete=models.CASCADE, related_name="rentals"
    )
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
        self.total_price = self.calculate_total_price()
        self.return_date = self.calculate_return_date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rental of {self.clothe.name} for {self.duration} days"