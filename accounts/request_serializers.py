from rest_framework import serializers

class SignInRequestSerializer(serializers.Serializer):
  email = serializers.EmailField()
  username = serializers.CharField()
  password = serializers.CharField()
  
class SignUpRequestSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField()
  username = serializers.CharField()
  age = serializers.IntegerField()
  job = serializers.CharField()
  gender = serializers.CharField()
