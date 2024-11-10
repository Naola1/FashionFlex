from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from shop.models import Clothes, Rental
from .forms import RentalForm
from .filters import ClotheFilter

# Home list view to show all available clothes with filtering and search functionality
def home_list_view(request):
    filterset = ClotheFilter(request.GET, queryset=Clothes.objects.all())
    search_query = request.GET.get('search', '')

    # Apply search filter if search_query is provided
    if search_query:
        clothes = filterset.qs.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    else:
        clothes = filterset.qs  # Use the filtered queryset from ClotheFilter directly

    context = {
        'clothes': clothes,
    }
    return render(request, 'shop/home.html', context)

# Detail view for a specific clothing item and to handle rental requests
def cloth_detail_view(request, cloth_id):
    cloth = get_object_or_404(Clothes, id=cloth_id)

    if request.method == "POST" and request.user.is_authenticated:
        duration = request.POST.get("duration")
        rental_date = request.POST.get("rental_date", timezone.now().date())

        try:
            price_per_day = cloth.price
            total_price = int(duration) * price_per_day

            rental_data = {
                "clothe": cloth,
                "user": request.user,
                "rental_date": rental_date,
                "duration": duration,
                "total_price": total_price,
            }
            rental = Rental(**rental_data)
            rental.save()

            return JsonResponse({'message': 'Rental created successfully!'}, status=201)
        except Clothes.DoesNotExist:
            return JsonResponse({"error": "Clothes not found."}, status=404)

    return render(request, 'shop/cloth_detail.html', {'cloth': cloth})

# View to show all clothes rented by the current user
@login_required
def rented_view(request):
    rented_clothes = Clothes.objects.filter(rental__user=request.user)
    context = {
        'rented_clothes': rented_clothes,
    }
    return render(request, 'shop/rented_list.html', context)
