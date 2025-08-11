from django.urls import path
from tasks.views import SignupView, LoginView, RequestOTPView, VerifyOTPView, LogoutView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/',LoginView.as_view(), name='login'),
    path('request-otp/', RequestOTPView.as_view(), name='request_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('logout/', LogoutView.as_view(), name='logout'),
      
]