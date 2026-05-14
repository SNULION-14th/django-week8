from rest_framework import serializers

class SignUpRequestSerializer(serializers.Serializer):
    password = serializers.CharField()
    username = serializers.CharField()
    work_start_time = serializers.TimeField()
    work_end_time = serializers.TimeField()

class SignInRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()