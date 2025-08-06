# from rest_framework_mongoengine import serializers
# from tasks.models import Task
# from datetime import datetime

# class TaskSerializer(serializers.DocumentSerializer):
#     """
#     Serializer for task model with validation
#     """
#     is_overdue = serializers.ReadOnlyField()

#     class Meta:
#         model = Task
#         fields = '__all__'
#         read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at', 'is_overdue']

#     def validate_due_date(self, value):
#         if value and value < datetime.utcnow():
#             raise serializers.ValidationError("Due cannot be a date in the past.")
#         return value

#     def validate_title(self,value):
#         if not value or not value.strip():
#             raise serializers.ValidationError("Title cannot be empty.")
#         if len(value.strip())<3:
#             raise serializers.ValidationError("Tile must be of minimum 3 characters length.")
#         return value.strip()

# class TaskCreateSerilaizer(TaskSerilaizer):
#     """
#     Serializer for creating tasks with additional validation
#     """
#     class Meta(TaskSerializer.Meta):
#         fields = ['title', 'description', 'due_date', 'priority']

# class TaskUpdateSerializer(serializers.DocumentSerializer):
#     """
#     Serializer for updating tasks(partially)
#     """
#     class Meta:
#         model = Task
#         fields = ['title', 'description', 'due_date', 'priority', 'is_completed']

#     def validate_due_date(self, value):
#         if value and value < datetime.utcnow():
#             raise serializers.ValidationError("Due cannot be a date in the past.")
#         return value

# class TaskListSerializer(serializers.DocumentSerializer):
#     """
#     Serializer for listing tasks
#     """
#     is_overdue = serializers.ReadOnlyField()

#     class Meta:
#         model = Task
#         fields = ['id', 'title', 'due_date', 'is_completed', 
#             'priority', 'created_at', 'is_overdue'] 