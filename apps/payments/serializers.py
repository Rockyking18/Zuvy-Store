from rest_framework import serializers
from .models import Payment, VendorPayout

# ── Input: buyer initiates payment for an order ───────────────────────
class PaymentInitiateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

# ── Output: Paystack session details returned to frontend ─────────────
class PaymentResponseSerializer(serializers.Serializer):
    payment_url = serializers.URLField()
    reference   = serializers.CharField()
    amount      = serializers.DecimalField(max_digits=10, decimal_places=2)

# ── Output: payment record for order detail view ──────────────────────
class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Payment
        fields = ['id','amount','method','status','transaction_ref','created_at']
        # gateway_data excluded — raw Paystack payload, internal only

# ── Output: vendor payout record ──────────────────────────────────────
class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model  = VendorPayout
        fields = ['id','amount','commission','status','payout_date','reference']
