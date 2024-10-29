from django.contrib import admin
from .models import Clothes, Rental


# Register your models here.
@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "availability", "rating", "stock", "condition", "views_count", "created_at", "updated_at"]
    list_filter = ["availability", "rating", "condition"]
    search_fields = ["name", "price", "availability", "rating", "stock", "condition", "views_count"]
    list_per_page = 20
@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ["clothe", "status", "rental_date", "duration", "total_price", "return_date", "late_fee", "is_extended", "created_at"]
    list_filter = ["status", "duration", "is_extended"]
    search_fields = ["clothe", "status", "rental_date", "duration", "total_price", "return_date", "late_fee", "is_extended"]
    list_per_page = 20
