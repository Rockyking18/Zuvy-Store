from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import (RegisterSerializer, LoginSerializer,
    UserProfileSerializer, ChangePasswordSerializer)
from apps.notifications.tasks import send_verification_email

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class   = RegisterSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_verification_email.delay(user.id)
        tokens = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'access': str(tokens.access_token),
            'refresh': str(tokens),
        }, status=201)

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class   = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if not user:
            return Response({'error':'Invalid credentials'}, status=401)
        if not user.is_verified:
            return Response({'error':'Email not verified'}, status=403)
        tokens = RefreshToken.for_user(user)
        return Response({'access':str(tokens.access_token),'refresh':str(tokens),'role':user.role})

class MeView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = UserProfileSerializer
    def get_object(self): return self.request.user

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail':'Password updated'})
