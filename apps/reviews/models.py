from django.db import models
from apps.core.models import TimeStampedModel
from apps.accounts.models import User
from apps.vendors.models import Vendor
from apps.products.models import Product


class Review(models.Model):
    buyer   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    vendor  = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='reviews')
    rating  = models.PositiveSmallIntegerField()  # 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        unique_together = ['buyer', 'product']  # one review per product per buyer
