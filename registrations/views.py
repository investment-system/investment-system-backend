from rest_framework import viewsets
from .models import RegistrationPayment
from .serializers import RegistrationPaymentSerializer

class RegistrationPaymentViewSet(viewsets.ModelViewSet):
    queryset = RegistrationPayment.objects.all().order_by('-created_at')
    serializer_class = RegistrationPaymentSerializer
