from decimal import Decimal

from django.db import models
from django.conf import settings
from django.db.models import Sum

from products.models import Product
from affiliates.models import Affiliate

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    affiliate = models.ForeignKey(
        Affiliate,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='orders'
    )

    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    is_paid = models.BooleanField(default=False)

    # ensures one-time commission creation
    commission_added = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_price = Decimal(self.product.price) * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} | {self.product.name} | {self.user}"


class CommissionTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ]

    affiliate = models.ForeignKey(
        Affiliate,
        on_delete=models.CASCADE,
        related_name='commissions'
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='commission'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission #{self.id} | {self.affiliate.user} | {self.amount}"


# Optional helper (keep this in Affiliate model ideally)
# shown here for reference
def affiliate_total_commission(affiliate):
    return affiliate.commissions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

class WithdrawRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    ]

    affiliate = models.ForeignKey('affiliates.Affiliate', on_delete=models.CASCADE, related_name='withdraw_requests')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Withdraw #{self.id} | {self.affiliate.user.email} | {self.amount} | {self.status}"
