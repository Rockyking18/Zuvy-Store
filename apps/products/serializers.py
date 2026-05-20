from rest_framework import serializers


class RecursiveField(serializers.Serializer):
    """Simple recursive serializer field for nested MPTT category trees."""

    def to_representation(self, value):
        parent_serializer = self.parent.parent.__class__
        serializer = parent_serializer(value, context=self.context)
        return serializer.data
from .models import Product, Category

# ── Category ──────────────────────────────────────────────────────────
class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)
    class Meta:
        model  = Category
        fields = ['id','name','icon','children']

# ── Product list (lightweight — used in search results & listings) ─────
class ProductListSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)
    category    = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model  = Product
        fields = ['id','name','price','stock','images',
                  'vendor_name','category','is_featured','created_at']

# ── Product detail (full view for a single product page) ──────────────
class ProductDetailSerializer(serializers.ModelSerializer):
    vendor   = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    class Meta:
        model  = Product
        fields = ['id','name','description','price','stock','images',
                  'vendor','category','is_featured','is_active','created_at']
    def get_vendor(self, obj):
        from apps.vendors.serializers import VendorPublicSerializer
        return VendorPublicSerializer(obj.vendor).data

# ── Product write (vendor creates or updates a product) ───────────────
class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ['name','description','price','stock','images','category','is_active']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than zero')
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock cannot be negative')
        return value

    def create(self, validated_data):
        vendor = self.context['request'].user.vendor
        return Product.objects.create(vendor=vendor, **validated_data)
