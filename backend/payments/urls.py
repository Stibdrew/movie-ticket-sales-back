from django.urls import path
from .views import CreatePaymentIntent, PaymentWebhookAPI, PaymentsRootView

# This file defines the URL patterns for the payments app in a Django project.
# It includes paths for creating a payment intent and handling payment webhooks.
app_name = "payments"
# The app_name is set to 'payments' to namespace the URLs for this app. 

urlpatterns = [
    path("", PaymentsRootView.as_view(), name="payments-root"),
    path("create-intent/", CreatePaymentIntent.as_view(), name="create-payment-intent"),
    path("webhook/", PaymentWebhookAPI.as_view(), name="payment-webhook"),
]
