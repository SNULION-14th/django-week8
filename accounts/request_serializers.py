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

class InterestListRequestSerializer(serializers.Serializer):
  user = SignInRequestSerializer()
  keyword = serializers.CharField()
  description = serializers.CharField()
  priority = serializers.IntegerField()

class InterestDetailRequestSerializer(serializers.Serializer):
  user = SignInRequestSerializer()
  keyword = serializers.CharField()
  description = serializers.CharField()
  priority = serializers.IntegerField()
