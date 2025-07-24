from rest_framework import viewsets
from .models import ProfitPayout
from .serializers import ProfitPayoutSerializer

class ProfitPayoutViewSet(viewsets.ModelViewSet):
    queryset = ProfitPayout.objects.all().order_by('-created_at')
    serializer_class = ProfitPayoutSerializer
