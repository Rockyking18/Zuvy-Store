from rest_framework import serializers
from .models import Review
from apps.orders.models import Order

# ── Input: buyer submits a review ────────────────────────────────────
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = ['product','vendor','rating','comment']

    def validate(self, data):
        buyer = self.context['request'].user
        product = data.get('product')
        # Buyer can only review a product they actually purchased and received
        purchased = Order.objects.filter(
            buyer=buyer,
            items__product=product,
            checkpoints__stage='COMPLETED'
        ).exists()
        if not purchased:
            raise serializers.ValidationError(
                'You can only review products from completed orders'
            )
        if Review.objects.filter(buyer=buyer, product=product).exists():
            raise serializers.ValidationError('You have already reviewed this product')
        return data

    def create(self, validated_data):
        return Review.objects.create(buyer=self.context['request'].user, **validated_data)

# ── Output: review shown on product/vendor page ───────────────────────
class ReviewSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.name', read_only=True)
    class Meta:
        model  = Review
        fields = ['id','buyer_name','rating','comment','created_at']
