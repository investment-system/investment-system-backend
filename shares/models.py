from django.db import models
from transactions.models import Transaction

class ShareRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    share_id = models.AutoField(primary_key=True)
    member_id = models.IntegerField()  # Later you can convert this to FK to a Member model
    project_name = models.CharField(max_length=255)
    share_date = models.DateField()
    share_return_rate = models.DecimalField(max_digits=5, decimal_places=2)
    expected_share_maturity_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    received_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="share_record")
    received_invoice_pdf = models.TextField(blank=True, null=True)
    share_duration_days = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project_name} ({self.member_id})"
