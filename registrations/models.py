from django.db import models
from datetime import date, timedelta
from transactions.models import Transaction

def default_share_date():
    return date.today()


class RegistrationPayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    member_id = models.IntegerField(null=True, blank=True)  # Use FK later when Member model is ready
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='registration_payment')
    payment_code = models.CharField(max_length=30, blank=True, null=True)
    confirmed_at = models.DateTimeField(default=default_share_date)
    created_at = models.DateTimeField(default=default_share_date)

    def __str__(self):
        return f"RegistrationPayment #{self.payment_id} | RM {self.transaction.amount}"
