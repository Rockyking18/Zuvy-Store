from django.urls import path
from .views import InitiatePaymentView, PaystackWebhookView, PayoutListView

urlpatterns = [
    path('initiate/',  InitiatePaymentView.as_view(),  name='payment-initiate'),
    path('webhook/',   PaystackWebhookView.as_view(),  name='payment-webhook'),
    path('payouts/',   PayoutListView.as_view(),       name='payout-list'),
]
# Mounted at: /api/payments/
# POST /api/payments/initiate/ — buyer starts payment
# POST /api/payments/webhook/  — Paystack posts payment result (public, HMAC-verified)
# GET  /api/payments/payouts/  — vendor views their payout history
