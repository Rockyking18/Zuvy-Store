from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ReviewCreateView(APIView):
	def post(self, request, *args, **kwargs):
		return Response(
			{'detail': 'Review creation is not implemented yet.'},
			status=status.HTTP_501_NOT_IMPLEMENTED,
		)


class ProductReviewListView(APIView):
	def get(self, request, *args, **kwargs):
		return Response(
			{'detail': 'Product review list is not implemented yet.'},
			status=status.HTTP_501_NOT_IMPLEMENTED,
		)


class VendorReviewListView(APIView):
	def get(self, request, *args, **kwargs):
		return Response(
			{'detail': 'Vendor review list is not implemented yet.'},
			status=status.HTTP_501_NOT_IMPLEMENTED,
		)
