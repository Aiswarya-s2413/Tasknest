from django.urls import path
from tasks.views import (TaskCreateView, TaskListView, TaskDetailView)

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<str:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
