from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from apps.core.permissions import IsBuyer, IsVendor, IsOrderParticipant
from apps.core.pagination import StandardPagination
from apps.products.models import Product
from apps.checkpoints.services import CheckpointService
from .models import Order, OrderItem
from .serializers import (OrderCreateSerializer, OrderDetailSerializer, OrderListSerializer)

class OrderCreateView(generics.CreateAPIView):
    """POST /api/orders/ — buyer places an order"""
    permission_classes = [IsBuyer]
    serializer_class   = OrderCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items_data = serializer.validated_data['items']
        address    = serializer.validated_data['shipping_address']
        total = 0
        order = Order.objects.create(buyer=request.user, total_amount=0, shipping_address=address)
        for item in items_data:
            product = Product.objects.select_for_update().get(id=item['product_id'])
            qty     = item['quantity']
            if product.stock < qty:
                raise serializers.ValidationError({product.name: 'Insufficient stock'})
            product.stock -= qty
            product.save(update_fields=['stock'])
            OrderItem.objects.create(
                order=order, product=product, vendor=product.vendor,
                quantity=qty, price=product.price
            )
            total += product.price * qty
        order.total_amount = total
        order.save(update_fields=['total_amount'])
        CheckpointService.advance(order, 'ORDER_PLACED')
        return Response(OrderDetailSerializer(order).data, status=201)

class OrderDetailView(generics.RetrieveAPIView):
    """GET /api/orders/:id/ — buyer or vendor views an order"""
    permission_classes = [IsOrderParticipant]
    serializer_class   = OrderDetailSerializer
    queryset           = Order.objects.prefetch_related('items','checkpoints')

class BuyerOrderListView(generics.ListAPIView):
    """GET /api/orders/ — buyer sees all their own orders"""
    permission_classes = [IsBuyer]
    serializer_class   = OrderListSerializer
    pagination_class   = StandardPagination
    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).order_by('-created_at')

class VendorOrderListView(generics.ListAPIView):
    """GET /api/orders/vendor/ — vendor sees orders that contain their products"""
    permission_classes = [IsVendor]
    serializer_class   = OrderListSerializer
    pagination_class   = StandardPagination
    def get_queryset(self):
        return Order.objects.filter(
            items__vendor__user=self.request.user
        ).distinct().order_by('-created_at')
