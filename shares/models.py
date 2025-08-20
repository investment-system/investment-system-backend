from django.db import models
from datetime import date, timedelta
from transactions.models import Transaction
from members.models import Member

def default_share_date():
    return date.today()

def default_maturity_date():
    return date.today() + timedelta(days=365)

class ShareRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    share_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='share_records')
    project_name = models.CharField(max_length=255, default='Katering Koperasi Masjid')

    share_date = models.DateField(default=default_share_date)
    share_return_rate = models.DecimalField(max_digits=5, decimal_places=2)

    expected_share_maturity_date = models.DateField(default=default_maturity_date)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    received_transaction = models.OneToOneField(Transaction,on_delete=models.CASCADE, related_name='share_record')

    share_duration_days = models.IntegerField(default=365)
    profit_payout_created = models.BooleanField(default=False)

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
