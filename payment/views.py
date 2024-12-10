import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import Payment
from shop.models import Rental  # We'll create this app next
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

# @login_required
# def initiate_payment(request, **kwargs):
#     try:
#         # Extract rental details from kwargs
#         cloth_id = kwargs.get('cloth_id')
#         duration = kwargs.get('duration')
#         rental_date = kwargs.get('rental_date')
#         return_date = kwargs.get('return_date')
#         total_price = kwargs.get('total_price')
#         notes = kwargs.get('notes', '')

#         # Create Stripe Checkout Session
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[{
#                 'price_data': {
#                     'currency': 'usd',
#                     'unit_amount': int(total_price * 100),  # Convert to cents
#                     'product_data': {
#                         'name': f'Rental for {duration} days',
#                     },
#                 },
#                 'quantity': 1,
#             }],
#             mode='payment',
#             success_url=request.build_absolute_uri(f'/payments/success?cloth_id={cloth_id}&duration={duration}&rental_date={rental_date}&return_date={return_date}&total_price={total_price}'),
#             cancel_url=request.build_absolute_uri('/payments/cancel'),
#             client_reference_id=str(request.user.id)
#         )

#         # Create a pending payment record
#         Payment.objects.create(
#             user=request.user,
#             cloth_id=cloth_id,
#             stripe_payment_intent=checkout_session.id,
#             amount=total_price,
#             status='pending'
#         )

#         return redirect(checkout_session.url)

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=403)

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

    # Create rental record
    rental = Rental.objects.create(
        user=request.user,
        cloth_id=cloth_id,
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