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
    
    def is_kyc_approved(self):
        return hasattr(self, 'kyc') and self.kyc.status == 'approved'


class VendorKYC(models.Model):
    KYC_PENDING    = 'pending'
    KYC_SUBMITTED  = 'submitted'
    KYC_REVIEWING  = 'reviewing'
    KYC_APPROVED   = 'approved'
    KYC_REJECTED   = 'rejected'

    KYC_STATUS_CHOICES = [
        (KYC_PENDING,   'Pending'),
        (KYC_SUBMITTED, 'Submitted'),
        (KYC_REVIEWING, 'Under Review'),
        (KYC_APPROVED,  'Approved'),
        (KYC_REJECTED,  'Rejected'),
    ]

    vendor                = models.OneToOneField('vendors.Vendor', on_delete=models.CASCADE, related_name='kyc')
    full_legal_name       = models.CharField(max_length=255)
    ghana_card_number     = models.CharField(max_length=20, unique=True)
    ghana_card_front      = models.ImageField(upload_to='kyc/ghana_card/')
    ghana_card_back       = models.ImageField(upload_to='kyc/ghana_card/')
    selfie_with_card      = models.ImageField(upload_to='kyc/selfies/')
    phone_number          = models.CharField(max_length=20)
    business_address      = models.TextField()
    business_reg_number   = models.CharField(max_length=100, blank=True)
    business_reg_cert     = models.ImageField(upload_to='kyc/business_certs/', blank=True)
    product_category      = models.ForeignKey('products.Category', on_delete=models.SET_NULL, null=True)
    status                = models.CharField(max_length=15, choices=KYC_STATUS_CHOICES, default=KYC_PENDING)
    rejection_reason      = models.TextField(blank=True)
    submitted_at          = models.DateTimeField(null=True, blank=True)
    reviewed_at           = models.DateTimeField(null=True, blank=True)
    reviewed_by           = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='kyc_reviews'
    )

    class Meta:
        db_table = 'vendor_kyc'

