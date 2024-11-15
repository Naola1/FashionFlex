from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from shop.models import Clothes, Rental, Category
from .forms import RentalForm
from .filters import ClotheFilter
from .forms import RentalForm

# Home list view to show all available clothes with filtering and search functionality
# views.py
from django.shortcuts import render
from django.db.models import Q
from .models import Clothes
from .filters import ClotheFilter

def get_all_child_categories(category):
    """
    Recursively get all child categories of a given category.
    """
    children = category.children.all()  # Get direct children
    all_children = list(children)  # Start with direct children
    for child in children:
        all_children.extend(get_all_child_categories(child))  # Add grandchildren, etc.
    return all_children

def home_list_view(request):
    filterset = ClotheFilter(request.GET, queryset=Clothes.objects.all())
    search_query = request.GET.get('search', '')
    category_slug = request.GET.get('category', '')

    if search_query:
        clothes = filterset.qs.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    elif category_slug:
        # Get the main category or subcategory
        category = get_object_or_404(Category, slug=category_slug)
        
        # Include clothes from the selected category and all its subcategories
        all_categories = [category] + get_all_child_categories(category)
        clothes = filterset.qs.filter(category__in=all_categories)
    else:
        clothes = filterset.qs

    context = {
        'clothes': clothes,
    }
    return render(request, 'shop/home.html', context)


# Detail view for a specific clothing item and to handle rental requests
def cloth_detail_view(request, cloth_id):
    # Get the current cloth item
    cloth = get_object_or_404(Clothes, id=cloth_id)

    # Fetch related clothes in the same category, excluding the current item
    related_clothes = Clothes.objects.filter(category=cloth.category).exclude(id=cloth_id)[:3]

    # Initialize the form
    form = RentalForm()

    if request.method == "POST" and request.user.is_authenticated:
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user
            rental.clothe = cloth
            rental.total_price = rental.calculate_total_price()
            rental.save()
            return JsonResponse({'message': 'Rental created successfully!'}, status=201)

    return render(request, 'shop/detail.html', {
        'cloth': cloth,
        'related_clothes': related_clothes,
        'form': form,
    })

# View to show all clothes rented by the current user
@login_required
def rented_view(request):
    rented_clothes = Clothes.objects.filter(rental__user=request.user)
    context = {
        'rented_clothes': rented_clothes,
    }
    return render(request, 'shop/rented_list.html', context)
