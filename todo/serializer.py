# post/serializers.py

from rest_framework.serializers import ModelSerializer
from .models import TodoList, Calendar, Routine

class TodoListSerializer(ModelSerializer):
    class Meta:
        model = TodoList
        fields = "__all__"
        
class RoutineSerializer(ModelSerializer):
    class Meta:
        model = Routine
        fields = "__all__"
        
class CalendarSerializer(ModelSerializer):
    class Meta:
        model = Calendar
        fields = "__all__"