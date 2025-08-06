from rest_framework.permissions import IsAuthenticated
from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # Attach current user to the task
            task = serializer.save(user=request.user)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects(user=request.user).order_by('-created_at')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
