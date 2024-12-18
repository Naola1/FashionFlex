import stripe
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import Payment
from shop.models import Rental  # We'll create this app next
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import timedelta
from django.views.decorators.csrf import csrf_protect

stripe.api_key = settings.STRIPE_SECRET_KEY



import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Payment
from shop.models import Clothes  # Import Clothes model
from shop.models import Rental

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def initiate_payment(request):
    try:
        # Extract rental details from POST data
        cloth_id = request.POST.get('cloth_id')
        duration = request.POST.get('duration')
        rental_date = request.POST.get('rental_date')
        return_date = request.POST.get('return_date')
        total_price = request.POST.get('total_price')
        notes = request.POST.get('notes', '')

        # Retrieve the Clothes instance
        cloth = Clothes.objects.get(id=cloth_id)

        # Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(float(total_price) * 100),  # Convert to cents
                    'product_data': {
                        'name': f'Rental for {duration} days',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/payments/success/?cloth_id={cloth_id}&duration={duration}&rental_date={rental_date}&return_date={return_date}&total_price={total_price}'),
            cancel_url=request.build_absolute_uri('/payments/cancel/'),
            client_reference_id=str(request.user.id)
        )

        # Create a pending payment record
        Payment.objects.create(
            user=request.user,
            cloth=cloth,  # Use the Clothes instance
            stripe_payment_intent=checkout_session.id,
            amount=total_price,
            status='pending'
        )

        return redirect(checkout_session.url)

    except Clothes.DoesNotExist:
        return JsonResponse({'error': 'Cloth not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)

@login_required
def payment_success(request):
    cloth_id = request.GET.get('cloth_id')
    duration = request.GET.get('duration')
    rental_date = request.GET.get('rental_date')
    return_date = request.GET.get('return_date')
    total_price = request.GET.get('total_price')

    clothe = Clothes.objects.get(id=cloth_id)
    # Create rental record
    rental = Rental.objects.create(
        user=request.user,
        clothe=clothe,
        duration=duration,
        rental_date=rental_date,
        return_date=return_date,
        total_price=total_price,
        status='active'
    )

    # Update Payment status
    Payment.objects.filter(
        user=request.user, 
        cloth_id=cloth_id, 
        status='pending'
    ).update(status='completed')

    return render(request, 'payments/success.html', {'rental': rental})

def payment_cancel(request):
    return render(request, 'payments/cancel.html')

@csrf_exempt
def stripe_webhook(request):
    # Handle Stripe webhook events if needed
    # This is an optional advanced configuration
    return HttpResponse(status=200)

# payments/views.py
import stripe
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Payment
from shop.models import Clothes, Rental

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def extend_rental(request, rental_id):
    """
    Handle payment for rental extension
    """
    try:
        # Get the existing rental
        rental = get_object_or_404(Rental, pk=rental_id, user=request.user)
        cloth = rental.clothe

        # Extract extension details
        days_to_extend = int(request.POST.get('days', 0))
        original_return_date = rental.return_date
        new_return_date = original_return_date + timedelta(days=days_to_extend)
        extension_price = days_to_extend * float(cloth.price)

        # Create Stripe Checkout Session for extension
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(extension_price * 100),  # Convert to cents
                    'product_data': {
                        'name': f'Rental Extension for {days_to_extend} days',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/payments/extension-success/?rental_id={rental_id}&days={days_to_extend}&extension_price={extension_price}'),
            cancel_url=request.build_absolute_uri('/payments/cancel/'),
            client_reference_id=str(request.user.id)
        )

        # Create a pending payment record for the extension
        Payment.objects.create(
            user=request.user,
            cloth=cloth,
            stripe_payment_intent=checkout_session.id,
            amount=extension_price,
            status='pending',
            payment_type='rental_extension'
        )

        return redirect(checkout_session.url)

    except Exception as e:
        messages.error(request, f'Payment initiation failed: {str(e)}')
        return redirect('rented_items')

@login_required
def extension_success(request):
    """
    Handle successful rental extension payment
    """
    rental_id = request.GET.get('rental_id')
    days_to_extend = int(request.GET.get('days', 0))
    extension_price = float(request.GET.get('extension_price', 0))

    try:
        # Get the rental
        rental = Rental.objects.get(id=rental_id, user=request.user)

        # Update rental details
        rental.return_date += timedelta(days=days_to_extend)
        rental.is_extended = True  # Set is_extended to True
        rental.extended_return_date = rental.return_date
        rental.total_price += extension_price
        rental.save()

        # Update payment status
        Payment.objects.filter(
            user=request.user,
            cloth_id=rental.clothe.id,
            status='pending',
            payment_type='rental_extension'
        ).update(status='completed')

        messages.success(request, f'Rental successfully extended by {days_to_extend} days.')
        return render(request, 'payments/extension_success.html', {
            'rental': rental,
            'days_extended': days_to_extend
        })

    except Rental.DoesNotExist:
        messages.error(request, 'Rental not found.')
        return redirect('rented_items')
    except Exception as e:
        messages.error(request, f'Extension processing failed: {str(e)}')
        return redirect('rented_items')