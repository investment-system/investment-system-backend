# transactions/models.py
from django.db import models

class Transaction(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('share', 'Share'),
        ('payment', 'Payment'),
        ('cancellation', 'Cancellation'),
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
    transaction_code = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    member_id = models.IntegerField(null=True, blank=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPE_CHOICES)
    reference_id = models.CharField(max_length=50, blank=True, null=True)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default='in')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_code:
            prefix = {
                'share': 'STKM',
                'payment': 'PTKM',
                'cancellation': 'CTKM',
                'withdrawal': 'WTKM',
                'deposit': 'DTKM',
            }.get(self.source_type, 'TKM')

            last = Transaction.objects.filter(source_type=self.source_type).order_by('-transaction_id').first()
            next_id = (last.transaction_id if last else 0) + 1
            self.transaction_code = f"{prefix}{next_id:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_code} | {self.source_type} | {self.direction} | RM {self.amount}"

