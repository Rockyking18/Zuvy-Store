from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


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
