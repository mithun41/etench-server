from decimal import Decimal
from django.db import models
from django.conf import settings
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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    affiliate = models.ForeignKey(Affiliate, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_paid = models.BooleanField(default=False)

    # ✅ Ensure commission is added only once
    commission_added = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-calculate total price
        self.total_price = Decimal(self.product.price) * self.quantity
        super().save(*args, **kwargs)

        # ✅ Automatically create commission if order is paid and not added yet
        if self.affiliate and self.is_paid and not self.commission_added:
            CommissionTransaction.objects.create(
                affiliate=self.affiliate,
                order=self,
                amount=Decimal(self.product.price) * self.quantity * (self.product.commission_rate / 100)
            )
            self.commission_added = True
            super().save(update_fields=['commission_added'])

    def __str__(self):
        return f"Order #{self.id} | {self.product.name} x {self.quantity} | {self.user}"


class CommissionTransaction(models.Model):
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE, related_name='commissions')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='commission')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission #{self.id} for {self.affiliate.user.email}: {self.amount}"


# ✅ Optional helper property for Affiliate model
# Add this inside your Affiliate model (affiliates/models.py)
@property
def total_commission(self):
    return self.commissions.aggregate(total=models.Sum('amount'))['total'] or 0
