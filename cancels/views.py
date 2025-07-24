from rest_framework import viewsets
from .models import CancellationRecord
from .serializers import CancellationRecordSerializer

class CancellationRecordViewSet(viewsets.ModelViewSet):
    queryset = CancellationRecord.objects.all()
    serializer_class = CancellationRecordSerializer
