from django.db import models, IntegrityError
from django.utils import timezone
from shares.models import ShareRecord
from transactions.models import Transaction
from members.models import Member


class CancellationRecord(models.Model):
    PAYOUT_TYPE_CHOICES = [
        ('pending', 'Pending'),
        ('full_transfer', 'Full Transfer'),
    ]

    cancellation_code = models.CharField(max_length=20, unique=True, blank=True)
    share = models.ForeignKey(ShareRecord, on_delete=models.CASCADE)
    member = models.ForeignKey(
        Member, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='cancellation_records'
    )
    cancellation_date = models.DateField(auto_now_add=True)
    payout_type = models.CharField(
        max_length=20, choices=PAYOUT_TYPE_CHOICES, default='pending'
    )
    penalty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=True)
    refund_amount = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # ✅ Always assign member from share
        self.member = self.share.member

        # Step 1: Calculate penalty and refund
        invested_amount = float(self.share.invested_amount)
        rate = float(self.penalty_rate) / 100
        self.penalty_amount = round(rate * invested_amount, 2)
        self.refund_amount = round(invested_amount - self.penalty_amount, 2)

        is_new = self._state.adding  # check if new instance

        if is_new:
            # Step 2: Generate cancellation code with retry logic
            max_retries = 5
            for attempt in range(max_retries):
                today_str = timezone.now().strftime("%Y%m%d")
                count_today = CancellationRecord.objects.filter(
                    cancellation_code__startswith=f"RFCKM-{today_str}"
                ).count() + 1

                self.cancellation_code = f"RFCKM-{today_str}-{count_today:04d}"

                try:
                    super().save(*args, **kwargs)
                    break
                except IntegrityError:
                    if attempt == max_retries - 1:
                        raise
        else:
            super().save(*args, **kwargs)

        # Step 3: Create or update transaction
        transaction_data = {
            'member': self.member,
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
