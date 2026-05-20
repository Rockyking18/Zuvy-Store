from celery import shared_task
from django.core.mail import send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# ── Helper: push a notification via WebSocket ─────────────────────────────────
def _push_ws_notification(user_id, notification):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        f'user_{user_id}',
        {
            'type': 'send.notification',
            'data': {
                'id': notification.id,
                'message': notification.message,
                'type': notification.type,
            }
        }
    )


# ── Email verification on registration ───────────────────────────────────────
@shared_task
def send_verification_email(user_id):
    from apps.accounts.models import User
    user = User.objects.get(id=user_id)
    send_mail(
        subject='Verify your Zuvy account',
        message=f'Hi {user.name}, please verify your email to activate your account.',
        from_email='noreply@zuvy.com',
        recipient_list=[user.email],
    )


# ── Notify vendor when a new order comes in ───────────────────────────────────
@shared_task
def notify_vendor_order(order_id):
    from apps.orders.models import Order
    from apps.notifications.models import Notification

    order   = Order.objects.prefetch_related('items__vendor__user').get(id=order_id)
    vendors = {item.vendor for item in order.items.all()}

    for vendor in vendors:
        notif = Notification.objects.create(
            user=vendor.user,
            message=f'New order #{order_id} received. Please review and accept.',
            type='order'
        )
        _push_ws_notification(vendor.user.id, notif)
        send_mail(
            subject=f'New Zuvy order #{order_id}',
            message=f'Hi {vendor.business_name}, you have a new order. Log in to accept it.',
            from_email='noreply@zuvy.com',
            recipient_list=[vendor.user.email],
        )


# ── Notify buyer when their order moves through a stage ──────────────────────
@shared_task
def notify_buyer_checkpoint(order_id, stage):
    from apps.orders.models import Order
    from apps.notifications.models import Notification

    order = Order.objects.select_related('buyer').get(id=order_id)
    labels = {
        'DISPATCHED':        'Your order has been dispatched.',
        'OUT_FOR_DELIVERY':  'Your order is out for delivery.',
        'DELIVERED':         'Your order has been delivered. Please confirm receipt.',
    }
    message = labels.get(stage, f'Your order status has been updated: {stage}')
    notif   = Notification.objects.create(
        user=order.buyer,
        message=message,
        type='order'
    )
    _push_ws_notification(order.buyer.id, notif)


# ── Trigger vendor payout when order is COMPLETED ────────────────────────────
@shared_task
def trigger_payout(order_id):
    import requests
    from django.conf import settings
    from apps.orders.models import Order
    from apps.payments.models import VendorPayout

    order = Order.objects.prefetch_related('items__vendor').get(id=order_id)

    # Group items by vendor (supports multi-vendor orders)
    vendor_totals = {}
    for item in order.items.all():
        vendor_totals.setdefault(item.vendor, 0)
        vendor_totals[item.vendor] += item.price * item.quantity

    for vendor, subtotal in vendor_totals.items():
        commission_rate = vendor.get_commission_rate()   # 0 for platform vendor
        commission      = subtotal * (commission_rate / 100)
        payout_amount   = subtotal - commission

        response = requests.post(
            'https://api.paystack.co/transfer',
            headers={'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'},
            json={
                'source':    'balance',
                'amount':    int(payout_amount * 100),  # Paystack uses pesewas
                'recipient': vendor.bank_account.get('recipient_code'),
                'reason':    f'Zuvy payout — Order #{order_id}',
            }
        )
        payout_ref = response.json()['data']['transfer_code']

        VendorPayout.objects.create(
            vendor=vendor,
            order=order,
            amount=payout_amount,
            commission=commission,
            status='processing',
            reference=payout_ref,
        )