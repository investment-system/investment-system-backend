from django.db import models
from transactions.models import Transaction
from shares.models import ShareRecord
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal

class ProfitPayout(models.Model):
    PAYOUT_TYPE_CHOICES = [
        ('pending', 'Pending'),
        ('full_transfer', 'Full Transfer'),
        ('partial', 'Partial Transfer'),
        ('reinvest', 'Reinvest All'),
    ]

    payout_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    share_record = models.ForeignKey(ShareRecord, on_delete=models.CASCADE)

    payout_type = models.CharField(max_length=20, choices=PAYOUT_TYPE_CHOICES, default='pending')
    invoice_file = models.FileField(upload_to='invoices/', blank=True, null=True)

    profit_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    profit_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def original_amount(self):
        try:
            return self.share_record.received_transaction.amount
        except:
            return Decimal('0.00')

    def save(self, *args, **kwargs):
        original_amount = self.original_amount

        self.profit_rate = self.profit_rate or self.share_record.share_return_rate
        self.profit_amount = (self.profit_rate / Decimal('100.00')) * original_amount

        if self.payout_type == 'full_transfer':
            self.refund_amount = original_amount + self.profit_amount
        elif self.payout_type == 'partial':
            self.refund_amount = self.profit_amount
        elif self.payout_type == 'reinvest':
            self.refund_amount = Decimal('0.00')

        super().save(*args, **kwargs)

        # ✅ Reinvestment logic
        if self.payout_type in ['partial', 'reinvest']:
            reinvest_amount = (
                original_amount if self.payout_type == 'partial'
                else original_amount + self.profit_amount
            )

            # Create new transaction
            new_transaction = Transaction.objects.create(
                member_id=self.transaction.member_id,
                amount=reinvest_amount,
                source_type='share',
                direction='in',
                payment_method='bank',
                created_at=timezone.now(),
            )

            # Create new share record
            ShareRecord.objects.create(
                member_id=self.transaction.member_id,
                project_name=self.share_record.project_name,
                share_date=date.today(),
                share_return_rate=self.profit_rate,
                expected_share_maturity_date=date.today() + timedelta(days=365),
                received_transaction=new_transaction,
                share_duration_days=365,
                status='active',
            )
