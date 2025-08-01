from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ShareRecord
from .serializers import ShareRecordSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ShareRecordViewSet(viewsets.ModelViewSet):
    queryset = ShareRecord.objects.select_related('received_transaction').all()
    serializer_class = ShareRecordSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'], url_path='add')
    def add_share_record(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
