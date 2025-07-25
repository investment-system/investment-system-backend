# transactions/models.py
from django.db import models
from django.utils import timezone  # ✅ Required for timezone.now()


class Transaction(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('share', 'Share'),
        ('payment', 'Payment'),
        ('cancellation', 'Cancellation'),
        ('registration_payments', 'Registration Payment'),
    ]

    DIRECTION_CHOICES = [
        ('in', 'In'),
        ('out', 'Out'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Card'),
        ('ewallet', 'E-Wallet'),
    ]

    transaction_id = models.AutoField(primary_key=True)
    transaction_code = models.CharField(max_length=30, unique=True, blank=True, editable=False)
    member_id = models.IntegerField(null=True, blank=True)
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPE_CHOICES)
    reference_id = models.CharField(max_length=50, blank=True, null=True)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default='in')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=250.00)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='bank_transfer')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_code:
            prefix = {
                'share': 'STKM',
                'payment': 'PTKM',
                'cancellation': 'CTKM',
                'withdrawal': 'WTKM',
                'deposit': 'DTKM',
                'registration_payments': 'RTKM',
            }.get(self.source_type, 'TKM')

            today_str = timezone.now().strftime("%Y%m%d")
            count_today = Transaction.objects.filter(
                transaction_code__startswith=f"{prefix}-{today_str}"
            ).count() + 1

            self.transaction_code = f"{prefix}-{today_str}-{count_today:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_code} | {self.source_type} | {self.direction} | RM {self.amount}"
