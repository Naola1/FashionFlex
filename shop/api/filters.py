import django_filters
from shop.models import Clothes, Category

class ClotheFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Search')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Category')

    class Meta:
        model = Clothes
        fields = {
            'gender': ['exact'],
            'size': ['exact'],
            'color': ['exact'],
            'style': ['exact'],
            'ethnicity': ['exact'],
            'item_type': ['exact'],
            'occasion': ['exact'],
            'price': ['lt', 'gt'],
            'availability': ['exact'],
        }