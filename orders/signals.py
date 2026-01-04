from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from decimal import Decimal

from .models import Order, CommissionTransaction


@receiver(post_save, sender=Order)
def create_commission_on_order_completed(sender, instance, **kwargs):
    if (
        instance.status != 'completed'
        or not instance.affiliate
        or instance.commission_added
    ):
        return

    with transaction.atomic():
        # Double-check inside transaction
        order = Order.objects.select_for_update().get(pk=instance.pk)

        if order.commission_added:
            return

        commission_rate = Decimal(order.product.commission_rate or 0) / Decimal(100)
        commission_amount = order.total_price * commission_rate

        CommissionTransaction.objects.create(
            affiliate=order.affiliate,
            order=order,
            amount=commission_amount
        )

        Order.objects.filter(pk=order.pk).update(commission_added=True)
