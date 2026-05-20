from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class NotificationListView(APIView):
	def get(self, request, *args, **kwargs):
		return Response(
			{'detail': 'Notification list is not implemented yet.'},
			status=status.HTTP_501_NOT_IMPLEMENTED,
		)


class MarkNotificationsReadView(APIView):
	def put(self, request, *args, **kwargs):
		return Response(
			{'detail': 'Mark notifications read is not implemented yet.'},
			status=status.HTTP_501_NOT_IMPLEMENTED,
		)
