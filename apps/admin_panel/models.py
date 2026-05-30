from django.db import models


class PlatformSettings(models.Model):
    default_commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    featured_listing_price  = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Platform Setting'
        verbose_name_plural = 'Platform Settings'

    def __str__(self):
        return 'Platform Settings'
