from django.db import models
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal
from transactions.models import Transaction
from shares.models import ShareRecord
from profits.utils import create_reinvestment


class ProfitPayout(models.Model):
    PAYOUT_TYPE_CHOICES = [
        ('pending', 'Pending'),
        ('full_transfer', 'Full Transfer'),
        ('partial', 'Partial Transfer'),
        ('reinvest', 'Reinvest All'),
    ]

    payout_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    share_record = models.OneToOneField(ShareRecord, on_delete=models.CASCADE)  # Each share can only be paid out once

    payout_type = models.CharField(max_length=20, choices=PAYOUT_TYPE_CHOICES, default='pending')
    invoice_file = models.FileField(upload_to='invoices/', blank=True, null=True)

    profit_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    profit_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    reinvestment_created = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def original_amount(self):
        return self.share_record.received_transaction.amount if self.share_record and self.share_record.received_transaction else Decimal('0.00')

    def save(self, *args, **kwargs):
        original = self.original_amount
        self.profit_rate = self.profit_rate or self.share_record.share_return_rate
        self.profit_amount = (self.profit_rate / Decimal('100.00')) * original

        if self.payout_type == 'full_transfer':
            self.refund_amount = original + self.profit_amount
        elif self.payout_type == 'partial':
            self.refund_amount = self.profit_amount
        elif self.payout_type == 'reinvest':
            self.refund_amount = Decimal('0.00')

        super().save(*args, **kwargs)

        # ✅ Create profit payout transaction (to member) if needed
        if self.payout_type in ['partial', 'full_transfer']:
            if not Transaction.objects.filter(reference_id=f"PROFIT-{self.pk}").exists():
                Transaction.objects.create(
                    member_id=self.transaction.member_id,
                    amount=self.refund_amount,
                    source_type='payment',
                    direction='out',
                    payment_method='bank_transfer',
                    reference_id=f"PROFIT-{self.pk}",
                    created_at=timezone.now(),
                )

        # ✅ Handle reinvestment (only for partial/reinvest)
        create_reinvestment(self)

    def __str__(self):
        return f"Payout {self.payout_id} - {self.payout_type} - RM{self.refund_amount}"
