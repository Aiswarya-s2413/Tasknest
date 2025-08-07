from django.urls import path
from tasks.views import (TaskCreateView, TaskListView)

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
]
