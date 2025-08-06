from django.urls import path
from tasks.views import SignupView, LoginView, OTPRequestSerializer,OTPVerifySerializer,CustomTokenObtainPairView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login.',LoginView.as_view(), name='login'),
    path('request-otp/', RequestOTPView.as_view(), name='request_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
      
]
