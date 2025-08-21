from rest_framework import viewsets, permissions
from .models import ProfitPayout
from .serializers import ProfitPayoutSerializer

class ProfitPayoutViewSet(viewsets.ModelViewSet):

    queryset = ProfitPayout.objects.all().order_by('-created_at')
    serializer_class = ProfitPayoutSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):

        queryset = super().get_queryset()
        member_id = self.request.query_params.get('member_id')
        if member_id:
            queryset = queryset.filter(member_id=member_id)
        return queryset
