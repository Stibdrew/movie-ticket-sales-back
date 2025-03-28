# payments/views.py
import stripe
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Order



stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntent(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        order_id = request.data.get('order_id')  # Get order_id from request

        if amount is None or order_id is None:
            return Response({"error": "Amount and order_id are required"}, status=400)

        # Convert amount to cents (Stripe expects the amount in the smallest currency unit)
        amount_in_cents = int(amount * 100)

        try:
            # Fetch the order
            order = Order.objects.get(id=order_id)

            # Create a payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency='php',
            )

            # Save payment_intent_id to Order
            order.payment_intent_id = intent.id
            order.save()

            return Response({'clientSecret': intent.client_secret}, status=200)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PaymentWebhookAPI(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            # Verify the webhook signature
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            # Invalid payload
            return Response(status=400)
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return Response(status=400)

        # Handle the event
        if event.get('type') == 'payment_intent.succeeded':
            payment_intent = event['data']['object']

            try:
                # Find the order using the payment_intent_id
                order = Order.objects.get(payment_intent_id=payment_intent['id'])
                # Update order status to 'paid'
                order.status = 'paid'
                order.save()
            except Order.DoesNotExist:
                return Response({'error': 'Order not found'}, status=404)

        return Response(status=200)

class PaymentsRootView(APIView):
    def get(self, request):
        return Response({
            "message": "Welcome to the Payments API!",
            "endpoints": {
                "create_intent": "/api/payments/create-intent/",
                "webhook": "/api/payments/webhook/"
            }
        })
