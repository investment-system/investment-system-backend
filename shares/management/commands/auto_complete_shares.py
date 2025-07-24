from django.core.management.base import BaseCommand
from django.utils import timezone
from shares.models import ShareRecord

class Command(BaseCommand):
    help = 'Auto-complete matured shares and trigger profit creation'

    def handle(self, *args, **options):
        today = timezone.now().date()
        matured_shares = ShareRecord.objects.filter(
            status='active',
            expected_share_maturity_date=today
        )

        count = 0
        for share in matured_shares:
            share.status = 'completed'
            share.save()  # Triggers the signal
            count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} matured share(s) marked as completed.'))
