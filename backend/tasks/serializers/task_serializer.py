from rest_framework_mongoengine import serializers as s
from tasks.models import Task


class TaskSerializer(s.DocumentSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'due_date',
            'scheduled_time',
            'priority',
            'is_completed',
            'created_at',
            'updated_at',
            'completed_at',
        ]
        read_only_fields = ['created_at', 'updated_at', 'completed_at', 'id']
