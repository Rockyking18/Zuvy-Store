from django.db import models
from apps.orders.models import Order

class Checkpoint(models.Model):
    ORDER_PLACED      = 'ORDER_PLACED'
    PAYMENT_CONFIRMED = 'PAYMENT_CONFIRMED'
    VENDOR_NOTIFIED   = 'VENDOR_NOTIFIED'
    ORDER_ACCEPTED    = 'ORDER_ACCEPTED'
    IN_PREPARATION    = 'IN_PREPARATION'
    DISPATCHED        = 'DISPATCHED'
    IN_TRANSIT        = 'IN_TRANSIT'
    OUT_FOR_DELIVERY  = 'OUT_FOR_DELIVERY'
    DELIVERED         = 'DELIVERED'
    COMPLETED         = 'COMPLETED'
    DISPUTED          = 'DISPUTED'
    REFUNDED          = 'REFUNDED'
    CANCELLED         = 'CANCELLED'

    STAGE_CHOICES = [
        (ORDER_PLACED, 'Order placed'),
        (PAYMENT_CONFIRMED, 'Payment confirmed'),
        (VENDOR_NOTIFIED, 'Vendor notified'),
        (ORDER_ACCEPTED, 'Order accepted'),
        (IN_PREPARATION, 'In preparation'),
        (DISPATCHED, 'Dispatched'),
        (IN_TRANSIT, 'In transit'),
        (OUT_FOR_DELIVERY, 'Out for delivery'),
        (DELIVERED, 'Delivered'),
        (COMPLETED, 'Completed'),
        (DISPUTED, 'Disputed'),
        (REFUNDED, 'Refunded'),
        (CANCELLED, 'Cancelled'),
    ]

    order     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='checkpoints')
    stage     = models.CharField(max_length=30, choices=STAGE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes     = models.TextField(blank=True)

    class Meta:
        db_table = 'checkpoints'
        ordering = ['timestamp']
