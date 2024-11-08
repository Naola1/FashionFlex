from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username']
    search_fields = ['email', 'username']
    # list_filter = ['role']
    list_per_page = 20
    # fieldsets = (
    #     (None, {'fields': ('email', 'username', 'role')}),
    #     ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name'