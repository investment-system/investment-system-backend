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
    transaction_code = models.CharField(max_length=20, unique=True, blank=True, editable=False)  # auto-generated
    member_id = models.IntegerField(null=True, blank=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPE_CHOICES)
    reference_id = models.IntegerField(null=True, blank=True)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_code:
            last_transaction = Transaction.objects.order_by('-transaction_id').first()
            next_id = (last_transaction.transaction_id if last_transaction else 0) + 1

            # Set prefix based on source_type
            prefix = "TKM"  # default
            if self.source_type == 'share':
                prefix = "STKM"

            self.transaction_code = f"{prefix}{next_id:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_code} | {self.source_type} | {self.direction} | RM {self.amount}"
