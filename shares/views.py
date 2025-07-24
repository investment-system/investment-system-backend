# views.py

from rest_framework import viewsets
from .models import ShareRecord
from .serializers import ShareRecordSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ShareRecordViewSet(viewsets.ModelViewSet):
    queryset = ShareRecord.objects.select_related('received_transaction').all()
    serializer_class = ShareRecordSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
