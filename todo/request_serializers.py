# ./todo/request_serializers.py

from rest_framework import serializers

from account.request_serializers import SignInRequestSerializer

class TodoListRequestSerializer(serializers.Serializer):
    user = SignInRequestSerializer()
    title = serializers.CharField()
    due_date = serializers.DateField()
    field = serializers.CharField(max_length=255)
    priority = serializers.IntegerField()
    
# Calendar용 Request Serializer
class CalendarRequestSerializer(serializers.Serializer):
    user = SignInRequestSerializer()
    title = serializers.CharField(max_length=255)
    date = serializers.DateField()
    field = serializers.CharField(max_length=255)
    
# Routine용 Request Serializer
class RoutineRequestSerializer(serializers.Serializer):
    user = SignInRequestSerializer()
    title = serializers.CharField(max_length=255)
    day = serializers.ChoiceField(choices=[
        ('MON'), ('TUE'), ('WED'),
        ('THU'), ('FRI'), ('SAT'), ('SUN') ])
    time = serializers.TimeField()
    field = serializers.CharField(max_length=255)