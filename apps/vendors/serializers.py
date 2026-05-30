from rest_framework import serializers
from .models import Vendor, VendorKYC

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

# ── KYC submission: vendor uploads their documents ────────────────────────────
class VendorKYCSerializer(serializers.ModelSerializer):
    class Meta:
        model  = VendorKYC
        fields = [
            'full_legal_name', 'ghana_card_number',
            'ghana_card_front', 'ghana_card_back',
            'selfie_with_card', 'phone_number',
            'business_address', 'business_reg_number',
            'business_reg_cert', 'product_category',
        ]

# ── KYC status: vendor checks where their application stands ──────────────────
class VendorKYCStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model  = VendorKYC
        fields = [
            'status', 'rejection_reason',
            'submitted_at', 'reviewed_at',
        ]
        read_only_fields = fields