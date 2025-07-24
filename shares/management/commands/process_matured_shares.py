from django.core.management.base import BaseCommand
from shares.models import ShareRecord
from profits.models import ProfitPayout
from transactions.models import Transaction
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Automatically process matured ShareRecords into ProfitPayout table'

    def handle(self, *args, **kwargs):
        today = date.today()
        matured_shares = ShareRecord.objects.filter(
            status='active',
            expected_share_maturity_date__lte=today
        )

        processed_count = 0

        for share in matured_shares:
            # Create ProfitPayout
            ProfitPayout.objects.create(
                transaction=share.received_transaction,
                share_record=share,
                payout_type='pending'  # admin can change this later
            )

            # Update share status to completed
            share.status = 'completed'
            share.save()

            processed_count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ {processed_count} matured shares processed successfully.'))
