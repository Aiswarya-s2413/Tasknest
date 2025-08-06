from django.urls import path
from tasks.views import SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),  
]
