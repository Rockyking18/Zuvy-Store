from rest_framework import serializers
from apps.accounts.models import User
from apps.vendors.models import Vendor
from apps.orders.models import Order
from .models import PlatformSettings

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id','email','name','role','is_verified','is_active','created_at']
        read_only_fields = ['id','email','created_at']

class AdminVendorSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model  = Vendor
        fields = ['id','owner_email','business_name','status',
                  'is_platform_vendor','commission_rate','rating','created_at']

class VendorStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['approved','rejected','suspended'])
    reason = serializers.CharField(required=False, allow_blank=True)

class AdminOrderSerializer(serializers.ModelSerializer):
    current_stage = serializers.SerializerMethodField()
    buyer_email   = serializers.EmailField(source='buyer.email', read_only=True)
    class Meta:
        model  = Order
        fields = ['id','buyer_email','total_amount','status','current_stage','created_at']
    def get_current_stage(self, obj):
        last = obj.checkpoints.last()
        return last.stage if last else None

class RefundSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    reason = serializers.CharField(max_length=1000)

class PlatformSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PlatformSettings
        fields = ['default_commission_rate','featured_listing_price']
