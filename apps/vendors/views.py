from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.core.permissions import IsVendor, IsApprovedVendor
from .models import Vendor
from .serializers import (VendorRegistrationSerializer,
    VendorDetailSerializer, VendorPublicSerializer)

class VendorRegisterView(generics.CreateAPIView):
    """POST /api/vendors/ — authenticated user registers as a vendor"""
    permission_classes = [IsAuthenticated]
    serializer_class   = VendorRegistrationSerializer

class VendorProfileView(generics.RetrieveUpdateAPIView):
    """GET/PUT /api/vendors/me/ — vendor views and edits their own profile"""
    permission_classes = [IsVendor]
    serializer_class   = VendorDetailSerializer
    def get_object(self): return self.request.user.vendor

class VendorPublicDetailView(generics.RetrieveAPIView):
    """GET /api/vendors/:id/ — public storefront, no auth required"""
    permission_classes = [AllowAny]
    serializer_class   = VendorPublicSerializer
    queryset           = Vendor.objects.filter(status='approved')
