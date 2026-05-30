from celery import shared_task
from django.core.mail import send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# Helper: push a notification via WebSocket
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


# Email verification on registration
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


# Notify vendor when a new order comes in 
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


# Notify buyer when their order moves through a stage
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

    # Auto-flag vendors with multiple disputes
@shared_task
def check_vendor_dispute_rate():
    from apps.vendors.models import Vendor
    from apps.checkpoints.models import Checkpoint
    from django.utils import timezone
    from datetime import timedelta

    period = timezone.now() - timedelta(days=30)
    vendors = Vendor.objects.filter(status='approved')

    for vendor in vendors:
        disputes = Checkpoint.objects.filter(
            stage='DISPUTED',
            order__items__vendor=vendor,
            timestamp__gte=period
        ).count()

        if disputes >= 3:
            vendor.status = 'suspended'
            vendor.save()
            notify_admin_vendor_suspended.delay(vendor.id, f'Auto-suspended: {disputes} disputes in 30 days')


@shared_task
def notify_admin_vendor_suspended(vendor_id, message):
    from apps.vendors.models import Vendor
    from apps.accounts.models import User
    from apps.notifications.models import Notification

    vendor = Vendor.objects.select_related('user').get(id=vendor_id)
    admins = User.objects.filter(role='admin')

    for admin in admins:
        Notification.objects.create(
            user=admin,
            message=message,
            type='system'
        )


# Trigger vendor payout when order is COMPLETED 
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

@shared_task
def notify_admin_kyc_submitted(kyc_id):
    from apps.vendors.models import VendorKYC
    from apps.accounts.models import User
    from apps.notifications.models import Notification

    kyc    = VendorKYC.objects.select_related('vendor__user').get(id=kyc_id)
    admins = User.objects.filter(role='admin')

    for admin in admins:
        Notification.objects.create(
            user=admin,
            message=f'New KYC submission from {kyc.vendor.business_name}. Please review.',
            type='system'
        )


@shared_task
def notify_vendor_kyc_approved(vendor_id):
    from apps.vendors.models import Vendor
    from apps.notifications.models import Notification

    vendor = Vendor.objects.select_related('user').get(id=vendor_id)
    Notification.objects.create(
        user=vendor.user,
        message='Your KYC has been approved. You can now list products on Zuvy!',
        type='system'
    )
    send_mail(
        subject='Zuvy KYC Approved',
        message=f'Hi {vendor.business_name}, your identity verification has been approved. Welcome to Zuvy!',
        from_email='noreply@zuvy.com',
        recipient_list=[vendor.user.email],
    )


@shared_task
def notify_vendor_kyc_rejected(vendor_id, reason):
    from apps.vendors.models import Vendor
    from apps.notifications.models import Notification

    vendor = Vendor.objects.select_related('user').get(id=vendor_id)
    Notification.objects.create(
        user=vendor.user,
        message=f'Your KYC was not approved. Reason: {reason}',
        type='system'
    )
    send_mail(
        subject='Zuvy KYC — Action Required',
        message=f'Hi {vendor.business_name}, your KYC was not approved.\n\nReason: {reason}\n\nPlease resubmit with the correct documents.',
        from_email='noreply@zuvy.com',
        recipient_list=[vendor.user.email],
    )