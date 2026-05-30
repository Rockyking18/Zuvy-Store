from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.permissions import IsAdmin
from apps.products.models import Product
from apps.products.serializers import ProductListSerializer
from apps.vendors.models import VendorKYC
from apps.admin_panel.serializers import AdminKYCSerializer
from apps.notifications.tasks import (
    notify_vendor_kyc_approved,
    notify_vendor_kyc_rejected,
)


class AdminKYCListView(generics.ListAPIView):
    """GET /api/admin/kyc/ — admin sees all KYC submissions"""
    permission_classes = [IsAdmin]
    serializer_class   = AdminKYCSerializer
    queryset = VendorKYC.objects.select_related('vendor__user').order_by('-submitted_at')
    filterset_fields   = ['status']

class AdminKYCReviewView(APIView):
    """POST /api/admin/kyc/:id/approve/ or /reject/"""
    permission_classes = [IsAdmin]

    def post(self, request, kyc_id, action):
        from django.utils import timezone
        kyc = VendorKYC.objects.get(id=kyc_id)
        if action == 'approve':
            kyc.status = 'approved'
            kyc.vendor.status = 'approved'  # also approve the vendor account
            kyc.vendor.save()
            notify_vendor_kyc_approved.delay(kyc.vendor.id)
        elif action == 'reject':
            reason = request.data.get('reason', '')
            kyc.status = 'rejected'
            kyc.rejection_reason = reason
            notify_vendor_kyc_rejected.delay(kyc.vendor.id, reason)
        kyc.reviewed_at = timezone.now()
        kyc.reviewed_by = request.user
        kyc.save()
        return Response({'detail': f'KYC {action}d successfully.'})


class AdminPendingProductListView(generics.ListAPIView):
    """GET /api/admin/products/pending/ — admin sees all pending product moderation queue"""
    permission_classes = [IsAdmin]
    serializer_class   = ProductListSerializer
    queryset           = Product.objects.filter(is_active=True, is_moderated=False).select_related('vendor','category').order_by('-created_at')
    filterset_fields   = ['vendor__id','category__id']


class AdminVendorListView(APIView):
	def get(self, request, *args, **kwargs):
		return Response({'detail': 'Admin vendor list is not implemented yet.'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class AdminVendorStatusView(APIView):
	def post(self, request, *args, **kwargs):
		return Response({'detail': 'Admin vendor status update is not implemented yet.'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class AdminUserListView(APIView):
	def get(self, request, *args, **kwargs):
		return Response({'detail': 'Admin user list is not implemented yet.'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class AdminOrderListView(APIView):
	def get(self, request, *args, **kwargs):
		return Response({'detail': 'Admin order list is not implemented yet.'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class AdminOrderRefundView(APIView):
	def post(self, request, *args, **kwargs):
		return Response({'detail': 'Admin order refund is not implemented yet.'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class AdminCheckpointOverrideView(APIView):
	def post(self, request, *args, **kwargs):
		return Response({'detail': 'Admin checkpoint override is not implemented yet.'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class AdminStatsView(APIView):
	def get(self, request, *args, **kwargs):
		return Response({'detail': 'Admin stats are not implemented yet.'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class AdminSettingsView(APIView):
	def get(self, request, *args, **kwargs):
		return Response({'detail': 'Admin settings are not implemented yet.'}, status=status.HTTP_501_NOT_IMPLEMENTED)
