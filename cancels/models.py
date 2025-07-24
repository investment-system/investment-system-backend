from django.db import models
from shares.models import ShareRecord
from transactions.models import Transaction  # ✅ Import your model
from django.utils import timezone
from decimal import Decimal

class CancellationRecord(models.Model):
    cancellation_code = models.CharField(max_length=20, unique=True, blank=True)
    share = models.ForeignKey(ShareRecord, on_delete=models.CASCADE)
    cancellation_date = models.DateField(auto_now_add=True)
    penalty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # e.g., 10.00 = 10%
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
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

        is_new = self._state.adding  # Track if new record

        super().save(*args, **kwargs)

        # Step 3: Create a transaction only for new records
        if is_new:
            Transaction.objects.create(
                transaction_code=self.cancellation_code,
                member_id=self.share.member_id,
                amount=self.refund_amount,
                source_type='cancellation',
                reference_id=self.cancellation_code,
                direction='out',
                payment_method='bank_transfer',
                created_at=timezone.now(),
            )

    def __str__(self):
        return f"{self.cancellation_code} - {self.share.project_name}"
