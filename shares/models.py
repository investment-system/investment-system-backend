from django.db import models
from datetime import date, timedelta
from transactions.models import Transaction

def default_share_date():
    return date.today()

def default_maturity_date():
    return date.today() + timedelta(days=365)

class ShareRecord(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    share_id = models.AutoField(primary_key=True)
    member_id = models.IntegerField()
    project_name = models.CharField(max_length=255, default='KKM')

    share_date = models.DateField(default=default_share_date)
    share_return_rate = models.DecimalField(max_digits=5, decimal_places=2)

    expected_share_maturity_date = models.DateField(default=default_maturity_date)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    received_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='share_record')
    share_duration_days = models.IntegerField(default=365)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_profit(self):
        return round(float(self.received_transaction.amount) * float(self.share_return_rate) / 100, 2)

    @property
    def invested_amount(self):
        return float(self.received_transaction.amount)

    @property
    def profit_rate(self):
        return float(self.share_return_rate)
