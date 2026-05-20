from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Checkpoint

VALID_TRANSITIONS = {
    'ORDER_PLACED':      ['PAYMENT_CONFIRMED', 'CANCELLED'],
    'PAYMENT_CONFIRMED': ['VENDOR_NOTIFIED'],
    'VENDOR_NOTIFIED':   ['ORDER_ACCEPTED', 'CANCELLED'],
    'ORDER_ACCEPTED':    ['IN_PREPARATION', 'CANCELLED'],
    'IN_PREPARATION':    ['DISPATCHED', 'CANCELLED'],
    'DISPATCHED':        ['IN_TRANSIT'],
    'IN_TRANSIT':        ['OUT_FOR_DELIVERY', 'DISPUTED'],
    'OUT_FOR_DELIVERY':  ['DELIVERED', 'DISPUTED'],
    'DELIVERED':         ['COMPLETED', 'DISPUTED'],
    'COMPLETED':         [],
    'DISPUTED':          ['REFUNDED', 'COMPLETED'],
    'REFUNDED':          [],
    'CANCELLED':         [],
}

class CheckpointService:

    @classmethod
    def advance(cls, order, new_stage, notes=''):
        current = order.checkpoints.last()
        current_stage = current.stage if current else None

        if current_stage and new_stage not in VALID_TRANSITIONS.get(current_stage, []):
            raise ValueError(f'Cannot transition from {current_stage} to {new_stage}')

        checkpoint = Checkpoint.objects.create(
            order=order, stage=new_stage, notes=notes
        )
        cls._broadcast(order, new_stage)
        cls._trigger_actions(order, new_stage)
        return checkpoint

    @classmethod
    def _broadcast(cls, order, stage):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'order_{order.id}',
            {'type': 'checkpoint.update',
             'data': {'order_id': order.id, 'stage': stage}}
        )

    @classmethod
    def _trigger_actions(cls, order, stage):
        from apps.notifications.tasks import (
            notify_vendor_order, notify_buyer_checkpoint, trigger_payout
        )
        if stage == 'VENDOR_NOTIFIED':
            notify_vendor_order.delay(order.id)
        elif stage in ['DISPATCHED', 'OUT_FOR_DELIVERY', 'DELIVERED']:
            notify_buyer_checkpoint.delay(order.id, stage)
        elif stage == 'COMPLETED':
            trigger_payout.delay(order.id)