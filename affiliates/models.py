import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Affiliate(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='affiliate'
    )

    referral_code = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        db_index=True
    )

    total_earned = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['referral_code']),
        ]

    def save(self, *args, **kwargs):
        if not self.referral_code:
            while True:
                code = uuid.uuid4().hex[:8]
                if not Affiliate.objects.filter(referral_code=code).exists():
                    self.referral_code = code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} ({self.referral_code})"

    # ✅ Must be inside the class
    @property
    def total_commission(self):
        total = self.commissions.filter(status='pending').aggregate(total=models.Sum('amount'))['total']
        pending_withdraw = self.withdraw_requests.filter(status__in=['pending', 'approved']).aggregate(total=models.Sum('amount'))['total'] or 0
        return (total or 0) - pending_withdraw

    def reduce_commission(self, amount):
        remaining = amount
        for c in self.commissions.filter(status='pending').order_by('created_at'):
            if remaining <= 0:
                break
            if c.amount <= remaining:
                remaining -= c.amount
                c.status = 'paid'
                c.save()
            else:
                c.amount -= remaining
                c.status = 'paid'
                c.save()
                remaining = 0
