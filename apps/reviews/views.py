from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg
from .models import Review


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

def update_vendor_rating(vendor):
    avg = Review.objects.filter(vendor=vendor).aggregate(Avg('rating'))['rating__avg']
    vendor.rating = round(avg, 2)
    vendor.save(update_fields=['rating'])