from rest_framework import generics, permissions
from .models import Member
from .serializers import RegisterSerializer, LoginSerializer, MemberSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

# Register
class RegisterView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = RegisterSerializer

# Login
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

# Authenticated user info
class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MemberSerializer

    def get_object(self):
        return self.request.user
