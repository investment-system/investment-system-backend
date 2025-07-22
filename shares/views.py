# views.py

from rest_framework import viewsets
from .models import ShareRecord
from .serializers import ShareRecordSerializer

class ShareRecordViewSet(viewsets.ModelViewSet):
    queryset = ShareRecord.objects.all().order_by('-created_at')
    serializer_class = ShareRecordSerializer
