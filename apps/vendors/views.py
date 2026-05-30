from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.core.permissions import IsVendor, IsApprovedVendor
from apps.notifications.tasks import notify_admin_kyc_submitted
from .models import Vendor
from .serializers import (VendorRegistrationSerializer,
    VendorDetailSerializer, VendorPublicSerializer, VendorKYCSerializer, VendorKYCStatusSerializer)

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

class SubmitKYCView(generics.CreateAPIView):
    """POST /api/vendors/kyc/ — vendor submits KYC documents"""
    permission_classes = [IsVendor]
    serializer_class   = VendorKYCSerializer

    def perform_create(self, serializer):
        from django.utils import timezone
        kyc = serializer.save(
            vendor=self.request.user.vendor,
            status='submitted',
            submitted_at=timezone.now()
        )
        # Notify admin
        notify_admin_kyc_submitted.delay(kyc.id)

class KYCStatusView(generics.RetrieveAPIView):
    """GET /api/vendors/kyc/ — vendor checks their KYC status"""
    permission_classes = [IsVendor]
    serializer_class   = VendorKYCStatusSerializer
    def get_object(self):
        return self.request.user.vendor.kyc