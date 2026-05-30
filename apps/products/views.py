from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import IsApprovedVendor
from apps.core.pagination import StandardPagination
from .models import Product
from .serializers import (ProductListSerializer, ProductDetailSerializer, ProductWriteSerializer)
from .filters import ProductFilter

class ProductListView(generics.ListAPIView):
    """GET /api/products/ — public product listing with filters"""
    permission_classes  = [AllowAny]
    serializer_class    = ProductListSerializer
    pagination_class    = StandardPagination
    filter_backends     = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class     = ProductFilter
    ordering_fields     = ['price','created_at']
    ordering            = ['-created_at']
    is_moderated         = True  # Only show products that have been approved by admin
    is_active            = True  # Only show products that are active
    queryset            = Product.objects.filter(is_active=True, is_moderated=True).select_related('vendor','category')

class ProductDetailView(generics.RetrieveAPIView):
    """GET /api/products/:id/ — single product full detail"""
    permission_classes = [AllowAny]
    serializer_class   = ProductDetailSerializer
    queryset           = Product.objects.filter(is_active=True, is_moderated=True)

class ProductCreateView(generics.CreateAPIView):
    """POST /api/products/ — approved vendor creates a product"""
    permission_classes = [IsApprovedVendor]
    serializer_class   = ProductWriteSerializer

class ProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """PUT/DELETE /api/products/:id/ — vendor edits or removes their own product"""
    permission_classes = [IsApprovedVendor]
    serializer_class   = ProductWriteSerializer
    def get_queryset(self):
        return Product.objects.filter(vendor__user=self.request.user)

class VendorProductListView(generics.ListAPIView):
    """GET /api/products/mine/ — vendor sees all their own products (incl inactive)"""
    permission_classes = [IsApprovedVendor]
    serializer_class   = ProductListSerializer
    def get_queryset(self):
        return Product.objects.filter(vendor__user=self.request.user)
