from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from tasks.serializers import UserSignupSerializer, UserLoginSerializer, OTPRequestSerializer, OTPVerifySerializer
from tasks.models import User
import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data

        # Set tokens in cookies
        response.set_cookie(
            key='access',
            value=data['access'],
            httponly=True,
            secure=False, 
            samesite='Lax',
            max_age=3600,  # 1 hour
        )

        response.set_cookie(
            key='refresh',
            value=data['refresh'],
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=7 * 24 * 3600,  # 7 days
        )

        # Remove tokens from response body
        del data['access']
        del data['refresh']

        return response


class SignupView(APIView):
    def post(self, request):
        Serializer = UserSignupSerializer(data=request.data)
        if Serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects(email=email).first():
                return Response({'error': 'User already exists'},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'message': 'User registered successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                "message": "Login successful",
                "user": {
                    "id": str(user.id),
                    "full_name": user.full_name,
                    "email": user.email,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class RequestOTPView(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects(email=email).first()

            if not user:
                return Response({'error': 'User not found. Please sign up first.'}, status=404)

            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
            user.save()

            # Send OTP to email 
            send_mail(
                subject="Your OTP for TaskNest Login",
                message=f"Your OTP is: {otp}. It expires in 5 minutes.",
                from_email="noreply@tasknest.com",
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({'message': 'OTP sent to your email.'}, status=200)
        return Response(serializer.errors, status=400)  

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            user = User.objects(email=email).first()
            if not user:
                return Response({'error': 'User not found'}, status=404)

            if user.otp != otp:
                return Response({'error': 'Invalid OTP'}, status=400)

            if not user.otp_expiry or user.otp_expiry < datetime.utcnow():
                return Response({'error': 'OTP expired'}, status=400)

            # clear OTP after use
            user.otp = None
            user.otp_expiry = None
            user.is_verified = True
            user.save()

            return Response({
                'message': 'OTP verified successfully',
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'full_name': user.full_name
                }
            }, status=200)
        return Response(serializer.errors, status=400)
