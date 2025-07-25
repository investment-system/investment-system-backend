from datetime import date, timedelta
from django.utils import timezone
from decimal import Decimal
from transactions.models import Transaction
from shares.models import ShareRecord

def create_reinvestment(payout):
    """
    Handles reinvestment logic based on payout type.
    Returns True if reinvestment was created, False otherwise.
    """
    if payout.reinvestment_created:
        return False  # Already reinvested

    original = payout.original_amount
    profit = payout.profit_amount or Decimal('0.00')

    if payout.payout_type == 'partial':
        reinvest_amount = original
    elif payout.payout_type == 'reinvest':
        reinvest_amount = original + profit
    else:
        return False  # Not a reinvestment type

    new_transaction = Transaction.objects.create(
        member_id=payout.transaction.member_id,
        amount=reinvest_amount,
        source_type='share',
        direction='in',
        payment_method='bank',
        created_at=timezone.now(),
    )

    payout.reinvestment_created = True
    payout.save(update_fields=['reinvestment_created'])
    return True
