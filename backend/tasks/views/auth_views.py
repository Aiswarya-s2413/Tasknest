from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from tasks.serializers import UserSignupSerializer, UserLoginSerializer, OTPRequestSerializer, OTPVerifySerializer
from tasks.models import User
import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects(email=email).first():
                return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            refresh = str(refresh)
            print(f"Access Token: {access}")
            print(f"Refresh Token: {refresh}")

            # Create response
            response = Response({
                "message": "Login successful",
                "user": {
                    "id": str(user.id),
                    "name": user.name,
                    "email": user.email,
                }
            }, status=status.HTTP_200_OK)

            # Set cookies
            response.set_cookie(
                key='access',
                value=access,
                httponly=True,
                secure=False,  # Change to True in production
                samesite='Lax',
                max_age=3600,
            )
            print("Access token set in cookie")

            response.set_cookie(
                key='refresh',
                value=refresh,
                httponly=True,
                secure=False,  # Change to True in production
                samesite='Lax',
                max_age=7 * 24 * 3600,
            )
            print("Refresh token set in cookie")

            return response

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
