from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, CommissionTransaction

@receiver(post_save, sender=Order)
def add_affiliate_commission(sender, instance, **kwargs):
    """
    When order status changes to 'completed', add product-specific commission to affiliate account.
    """
    if instance.status == 'completed' and instance.affiliate and not instance.commission_added:
        commission_amount = instance.total_price * (instance.product.commission_rate / Decimal('100'))

        # Update affiliate account
        instance.affiliate.balance += commission_amount
        instance.affiliate.total_earned += commission_amount
        instance.affiliate.save()

        # Create audit record
        CommissionTransaction.objects.create(
            affiliate=instance.affiliate,
            order=instance,
            amount=commission_amount
        )

        # Mark as added
        instance.commission_added = True
        instance.save(update_fields=['commission_added'])
