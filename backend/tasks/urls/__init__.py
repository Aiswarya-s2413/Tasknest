from django.urls import path, include

urlpatterns = [
    path('', include('tasks.urls.auth_urls')),  
]