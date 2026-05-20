from django.db import models

class TimeStampedModel(models.Model):
    """
    Abstract base class. Every model in Zuvy extends this.
    Provides created_at and updated_at automatically.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
