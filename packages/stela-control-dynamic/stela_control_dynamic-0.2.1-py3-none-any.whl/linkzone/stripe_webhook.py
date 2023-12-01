from django.views.decorators.csrf import csrf_exempt
import stripe, requests
from django.http import JsonResponse
from django.conf import settings
from .views import orderGenerator


@csrf_exempt
def stripePayment(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.WEBHOOK_SECRET
        )

    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e
    
    # Passed signature verification
    if event['type'] == 'charge.failed':
      print('payment failed')
    elif event['type'] == 'charge.dispute.created':
      print('dispute payment')
    elif event['type'] == 'payment_intent.created':
      print('payment intent')
    elif event['type'] == 'payment_intent.succeeded':
        data = event.data.object.id
        orderGenerator(data)
        # ... handle other event types
    return JsonResponse({'success': True})


