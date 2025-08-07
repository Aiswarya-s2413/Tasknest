from django.urls import path, include

urlpatterns = [
    path('', include('tasks.urls.auth_urls')),
    path('', include('tasks.urls.task_urls')),  
]