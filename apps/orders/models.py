from django.db import models
from apps.accounts.models import User
from apps.vendors.models import Vendor
from apps.products.models import Product

class Order(models.Model):
    PENDING   = 'pending'
    ACTIVE    = 'active'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [(PENDING,'Pending'),(ACTIVE,'Active'),(COMPLETED,'Completed'),(CANCELLED,'Cancelled')]

    buyer        = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    shipping_address = models.JSONField(default=dict)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    order     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product   = models.ForeignKey(Product, on_delete=models.PROTECT)
    vendor    = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    quantity  = models.PositiveIntegerField()
    price     = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot at time of order

    class Meta:
        db_table = 'order_items'
