from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import ShareRecord
from .serializers import ShareRecordSerializer

class ShareRecordViewSet(viewsets.ModelViewSet):
    queryset = ShareRecord.objects.select_related('received_transaction').all()
    serializer_class = ShareRecordSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
