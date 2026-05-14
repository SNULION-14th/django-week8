from rest_framework.serializers import ModelSerializer
from .models import Task, Task_history, Scheduled_task

class TaskSerializer(ModelSerializer):
  class Meta:
    model = Task
    fields = "__all__"

class TaskHistorySerializer(ModelSerializer):
  class Meta:
    model = Task_history
    fields = "__all__"

class ScheduledTaskSerializer(ModelSerializer):
  class Meta:
    model = Scheduled_task
    fields = "__all__"