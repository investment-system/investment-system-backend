from rest_framework import viewsets, permissions
from .models import CancellationRecord
from .serializers import CancellationRecordSerializer


class CancellationRecordViewSet(viewsets.ModelViewSet):
    queryset = CancellationRecord.objects.all()
    serializer_class = CancellationRecordSerializer
    permission_classes = [permissions.IsAdminUser]


    def get_queryset(self):

        queryset = super().get_queryset()
        member_id = self.request.query_params.get('member_id')
        if member_id:
            queryset = queryset.filter(member_id=member_id)
        return queryset