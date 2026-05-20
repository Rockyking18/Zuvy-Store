from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from apps.vendors.models import Vendor

class Category(MPTTModel):
    name   = models.CharField(max_length=100)
    icon   = models.CharField(max_length=50, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:
        db_table = 'categories'

class Product(models.Model):
    vendor      = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name        = models.CharField(max_length=255)
    description = models.TextField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField(default=0)
    images      = models.JSONField(default=list)  # list of S3 URLs
    is_active   = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

    def reduce_stock(self, quantity):
        if self.stock < quantity:
            raise ValueError(f'Insufficient stock for {self.name}')
        self.stock -= quantity
        self.save(update_fields=['stock'])
