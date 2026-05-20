from rest_framework import serializers
from .models import Checkpoint

# ── Output: one checkpoint stage in an order's timeline ──────────────
class CheckpointSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Checkpoint
        fields = ['id','stage','timestamp','notes']

# ── Input: vendor or system advancing an order to the next stage ─────
class CheckpointCreateSerializer(serializers.Serializer):
    stage = serializers.ChoiceField(choices=Checkpoint.STAGE_CHOICES)
    notes = serializers.CharField(required=False, allow_blank=True, default='')

# ── Input: buyer raising a dispute ────────────────────────────────────
class DisputeSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=1000)

# ── Input: admin issuing a refund ─────────────────────────────────────
class RefundSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    reason = serializers.CharField(max_length=1000)
