from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.permissions import IsBuyer, IsVendor, IsAdmin, IsOrderParticipant
from apps.orders.models import Order
from .models import Checkpoint
from .serializers import CheckpointSerializer, CheckpointCreateSerializer, DisputeSerializer
from .services import CheckpointService

class CheckpointListView(generics.ListAPIView):
    """GET /api/orders/:id/checkpoints/ — full stage history for an order"""
    permission_classes = [IsOrderParticipant]
    serializer_class   = CheckpointSerializer
    def get_queryset(self):
        order = Order.objects.get(pk=self.kwargs['order_id'])
        self.check_object_permissions(self.request, order)
        return Checkpoint.objects.filter(order=order)

class AdvanceCheckpointView(APIView):
    """POST /api/orders/:id/checkpoints/ — vendor advances the order stage"""
    permission_classes = [IsVendor]
    def post(self, request, order_id):
        order = Order.objects.get(pk=order_id, items__vendor__user=request.user)
        serializer = CheckpointCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cp = CheckpointService.advance(
            order,
            serializer.validated_data['stage'],
            serializer.validated_data.get('notes','')
        )
        return Response(CheckpointSerializer(cp).data, status=201)

class ConfirmDeliveryView(APIView):
    """POST /api/orders/:id/confirm-delivery/ — buyer confirms receipt → COMPLETED"""
    permission_classes = [IsBuyer]
    def post(self, request, order_id):
        order = Order.objects.get(pk=order_id, buyer=request.user)
        cp = CheckpointService.advance(order, 'COMPLETED')
        return Response({'detail': 'Order completed. Payout initiated.'})

class DisputeView(APIView):
    """POST /api/orders/:id/dispute/ — buyer raises a dispute"""
    permission_classes = [IsBuyer]
    def post(self, request, order_id):
        order = Order.objects.get(pk=order_id, buyer=request.user)
        serializer = DisputeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cp = CheckpointService.advance(order, 'DISPUTED', serializer.validated_data['reason'])
        return Response({'detail': 'Dispute raised. Admin will review shortly.'})

class CancelOrderView(APIView):
    """POST /api/orders/:id/cancel/ — buyer or vendor cancels an order"""
    permission_classes = [IsOrderParticipant]
    def post(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        self.check_object_permissions(request, order)
        cp = CheckpointService.advance(order, 'CANCELLED', 'Cancelled by user')
        return Response({'detail': 'Order cancelled.'})
