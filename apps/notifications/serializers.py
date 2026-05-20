from rest_framework import serializers
from .models import Notification

# ── Output: notification item ─────────────────────────────────────────
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Notification
        fields = ['id','message','type','is_read','created_at']

# ── Input: mark one or many notifications as read ─────────────────────
class MarkReadSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text='List of notification IDs to mark as read. Pass empty list to mark all.'
    )
