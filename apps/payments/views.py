from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class InitiatePaymentView(APIView):
	def post(self, request, *args, **kwargs):
		return Response(
			{'detail': 'Payment initiation is not implemented yet.'},
			status=status.HTTP_501_NOT_IMPLEMENTED,
		)


class PaystackWebhookView(APIView):
	def post(self, request, *args, **kwargs):
		return Response(
			{'detail': 'Paystack webhook handler is not implemented yet.'},
			status=status.HTTP_501_NOT_IMPLEMENTED,
		)


class PayoutListView(APIView):
	def get(self, request, *args, **kwargs):
		return Response(
			{'detail': 'Payout list is not implemented yet.'},
			status=status.HTTP_501_NOT_IMPLEMENTED,
		)
