from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from shop.models import Clothes, Rental, Category
from .forms import RentalForm
from .filters import ClotheFilter
from .forms import RentalForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decimal import Decimal
from .forms import RentalForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def home_view(request):
    # Filter available clothes based on stock or other availability indicator
    # Modify this condition based on your actual model
    available_clothes = Clothes.objects.filter(stock__gt=0)
    
    # Apply search and category filters
    filterset = ClotheFilter(request.GET, queryset=available_clothes)
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

    # Pagination
    paginator = Paginator(clothes, 10)  # 10 items per page
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'clothes': page_obj,
        'paginator': paginator,
        'page_obj': page_obj,
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
        'price': float(cloth.price),
    })

# View to show all clothes rented by the current user
@login_required
def rented_view(request):
    rented_clothes = Clothes.objects.filter(rental__user=request.user)
    context = {
        'rented_clothes': rented_clothes,
    }
    return render(request, 'shop/rented_list.html', context)

@login_required
@require_POST
def process_payment(request):
    try:
        # Get form data
        cloth_id = request.POST.get('cloth_id')
        duration = int(request.POST.get('rental_duration'))
        start_date = request.POST.get('rental_start_date')
        notes = request.POST.get('rental_notes')
        total_amount = Decimal(request.POST.get('total_amount'))

        # Get the cloth
        cloth = get_object_or_404(Clothes, id=cloth_id)

        # Validate availability
        if not cloth.is_available:
            return JsonResponse({
                'success': False,
                'message': 'This item is no longer available.'
            }, status=400)

        # Process payment (integrate with your payment gateway here)
        # This is where you'd integrate with Stripe, PayPal, etc.
        try:
            # Placeholder for payment processing
            payment_successful = True  # Replace with actual payment processing
            
            if payment_successful:
                # Create rental order
                rental_order = Rental.objects.create(
                    user=request.user,
                    cloth=cloth,
                    duration=duration,
                    start_date=start_date,
                    total_amount=total_amount,
                    notes=notes,
                    status='confirmed'
                )
                
                # Update cloth availability
                cloth.is_available = False
                cloth.save()
                
                # Redirect to success page
                return redirect('rental_success', order_id=rental_order.id)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Payment processing failed. Please try again.'
            }, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }, status=400)