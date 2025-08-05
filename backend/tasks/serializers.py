from rest_framework import serializers
from .models import tasknestdb

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'