from rest_framework_mongoengine.viewsets import ModelViewSet
from tasks.models import Task
from tasks.serializers import TaskSerializer

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all()
