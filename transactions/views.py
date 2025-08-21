from decimal import Decimal
from django.db.models import Sum
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import TransactionSerializer, TransactionStatsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Transaction


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


    @action(detail=False, methods=['post'], url_path='add')
    def add_transaction(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        registration_amount = Transaction.objects.filter(
            source_type='registration_payments', direction='in'
        ).aggregate(total=Sum('amount'))['total'] or 0

        share_amount = Transaction.objects.filter(
            source_type='share', direction='in'
        ).aggregate(total=Sum('amount'))['total'] or 0

        share_completed = Transaction.objects.filter(
            direction='out'
        ).exclude(source_type='cancellation').count()

        share_canceled = Transaction.objects.filter(
            source_type='cancellation'
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_transactions = Transaction.objects.count()
        total_balance = Transaction.objects.filter(direction='in').aggregate(total=Sum('amount'))['total'] or 0
        money_in = Transaction.objects.filter(direction='in').aggregate(total=Sum('amount'))['total'] or 0
        money_out = Transaction.objects.filter(direction='out').aggregate(total=Sum('amount'))['total'] or 0
        money_reinvest = Transaction.objects.filter(direction='reinvest').aggregate(total=Sum('amount'))['total'] or 0

        expected_profit = Decimal(share_amount) * Decimal('0.10')

        data = {
            'registration_amount': registration_amount,
            'share_amount': share_amount,
            'share_completed': share_completed,
            'share_canceled': share_canceled,
            'total_transactions': total_transactions,
            'total_balance': total_balance,
            'money_in': money_in,
            'money_out': money_out,
            'money_reinvest': money_reinvest,
            'expected_profit': expected_profit,
        }

        serializer = TransactionStatsSerializer(data)  # ✅ fixed
        return Response(serializer.data)

class UserTransactionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            member = request.user.member
        except AttributeError:
            return Response({"detail": "Member profile not found."}, status=status.HTTP_404_NOT_FOUND)

        transactions = Transaction.objects.filter(member=member)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

class UserTransactionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        try:
            transaction = Transaction.objects.get(pk=pk, member__user=user)
        except Transaction.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

class AdminMemberTransactionListAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]  # admin-only

    def get(self, request, member_id):
        transactions = Transaction.objects.filter(member_id=member_id).order_by('-created_at')
        if not transactions.exists():
            return Response(
                {"detail": "No transactions found for this member."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MemberStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, member_id):
        transactions = Transaction.objects.filter(member_id=member_id)

        if not transactions.exists():
            return Response(
                {"detail": "No transactions found for this member."},
                status=status.HTTP_404_NOT_FOUND
            )

        share_amount = transactions.filter(
            source_type='share', direction='in'
        ).aggregate(total=Sum('amount'))['total'] or 0

        profit = Decimal(share_amount) * Decimal('0.10')  # adjust formula
        money_in = transactions.filter(direction='in').aggregate(total=Sum('amount'))['total'] or 0
        money_out = transactions.filter(direction='out').aggregate(total=Sum('amount'))['total'] or 0

        data = {
            "member_id": member_id,
            "share_amount": share_amount,
            "profit": profit,
            "money_in": money_in,
            "money_out": money_out,
        }

        return Response(data, status=status.HTTP_200_OK)
