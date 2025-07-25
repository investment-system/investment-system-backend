from django.db import models
from shares.models import ShareRecord
from transactions.models import Transaction
from django.utils import timezone
from decimal import Decimal


class CancellationRecord(models.Model):
    PAYOUT_TYPE_CHOICES = [
        ('pending', 'Pending'),
        ('full_transfer', 'Full Transfer'),
    ]

    cancellation_code = models.CharField(max_length=20, unique=True, blank=True)
    share = models.ForeignKey(ShareRecord, on_delete=models.CASCADE)
    cancellation_date = models.DateField(auto_now_add=True)
    payout_type = models.CharField(max_length=20, choices=PAYOUT_TYPE_CHOICES, default='pending')
    penalty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Step 1: Calculate penalty & refund
        invested_amount = float(self.share.invested_amount)
        rate = float(self.penalty_rate) / 100
        self.penalty_amount = round(rate * invested_amount, 2)
        self.refund_amount = round(invested_amount - self.penalty_amount, 2)

        # Step 2: Generate cancellation code if not set
        if not self.cancellation_code:
            last_id = CancellationRecord.objects.count() + 1
            self.cancellation_code = f"RFKM{last_id:04d}"

        is_new = self._state.adding  # New record?

        super().save(*args, **kwargs)

        # Step 3: Create or update the transaction
        transaction_data = {
            'member_id': self.share.member_id,
            'amount': self.refund_amount,
            'source_type': 'cancellation',
            'reference_id': self.cancellation_code,
            'direction': 'out',
            'payment_method': 'bank_transfer',
            'created_at': timezone.now(),
        }

        if is_new:
            Transaction.objects.create(
                transaction_code=self.cancellation_code,
                **transaction_data
            )
        else:
            Transaction.objects.filter(reference_id=self.cancellation_code).update(
                amount=self.refund_amount
            )

    def __str__(self):
        return f"{self.cancellation_code} - {self.share.project_name}"
