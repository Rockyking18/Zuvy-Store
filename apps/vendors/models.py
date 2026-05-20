from django.db import models
from apps.accounts.models import User

class Vendor(models.Model):
    PENDING  = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    SUSPENDED = 'suspended'
    STATUS_CHOICES = [
        (PENDING, 'Pending'), (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'), (SUSPENDED, 'Suspended'),
    ]

    user              = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name     = models.CharField(max_length=255)
    description       = models.TextField(blank=True)
    logo_url          = models.ImageField(upload_to='vendor_logos/', blank=True)
    status            = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    rating            = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    is_platform_vendor = models.BooleanField(default=False)  # Admin's own store
    commission_rate   = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bank_account      = models.JSONField(default=dict)  # Paystack recipient details
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vendors'

    def get_commission_rate(self):
        from django.conf import settings
        if self.is_platform_vendor:
            return 0  # No commission for platform's own store
        return self.commission_rate or settings.DEFAULT_COMMISSION_RATE

