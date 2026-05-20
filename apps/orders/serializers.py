from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.models import Product

# ── Input: one line in the buyer's cart ──────────────────────────────
class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity   = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f'Product {value} not found or inactive')
        return value

# ── Input: the full order from the buyer ─────────────────────────────
class OrderCreateSerializer(serializers.Serializer):
    items            = OrderItemInputSerializer(many=True)
    shipping_address = serializers.JSONField()

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError('Order must contain at least one item')
        return items

# ── Output: one item in an order response ────────────────────────────
class OrderItemDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    vendor_name  = serializers.CharField(source='vendor.business_name', read_only=True)
    class Meta:
        model  = OrderItem
        fields = ['id','product_id','product_name','vendor_name','quantity','price']

# ── Output: full order detail ─────────────────────────────────────────
class OrderDetailSerializer(serializers.ModelSerializer):
    items        = OrderItemDetailSerializer(many=True, read_only=True)
    buyer_name   = serializers.CharField(source='buyer.name', read_only=True)
    current_stage = serializers.SerializerMethodField()
    class Meta:
        model  = Order
        fields = ['id','buyer_name','items','total_amount',
                  'status','current_stage','shipping_address','created_at']
    def get_current_stage(self, obj):
        last = obj.checkpoints.last()
        return last.stage if last else None

# ── Output: lightweight order list ────────────────────────────────────
class OrderListSerializer(serializers.ModelSerializer):
    current_stage = serializers.SerializerMethodField()
    item_count    = serializers.IntegerField(source='items.count', read_only=True)
    class Meta:
        model  = Order
        fields = ['id','total_amount','status','current_stage','item_count','created_at']
    def get_current_stage(self, obj):
        last = obj.checkpoints.last()
        return last.stage if last else None
