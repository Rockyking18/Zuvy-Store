from rest_framework import serializers
from .models import Vendor

# ── Registration: vendor submits their business details ───────────────
class VendorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Vendor
        fields = ['business_name','description','logo_url']

    def create(self, validated_data):
        user = self.context['request'].user
        if hasattr(user, 'vendor'):
            raise serializers.ValidationError('You already have a vendor profile')
        return Vendor.objects.create(user=user, **validated_data)

# ── Public: shown to buyers browsing a vendor storefront ──────────────
class VendorPublicSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='business_name')
    class Meta:
        model  = Vendor
        fields = ['id','name','description','logo_url','rating','created_at']

# ── Detail: vendor sees their own full profile including status ────────
class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Vendor
        fields = ['id','business_name','description','logo_url',
                  'status','rating','is_platform_vendor',
                  'commission_rate','created_at']
        read_only_fields = ['id','status','rating','is_platform_vendor',
                            'commission_rate','created_at']

# ── Admin approval: admin sees all fields ─────────────────────────────
class VendorAdminSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model  = Vendor
        fields = ['id','owner_email','business_name','status',
                  'is_platform_vendor','commission_rate','rating','created_at']
