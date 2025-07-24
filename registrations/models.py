from django.db import models
from transactions.models import Transaction

class RegistrationPayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    member_id = models.IntegerField(null=True, blank=True)  # Use FK later when Member model is ready
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='registration_payment')
    payment_code = models.CharField(max_length=30, blank=True, null=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RegistrationPayment #{self.payment_id} | RM {self.transaction.amount}"
