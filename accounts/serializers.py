from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from .models import Interest

User = get_user_model()

class UserIdUsernameSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "username"]

class UserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "username", "password", "age", "job", "gender", "created_at"]

class InterestSerializer(ModelSerializer):
  class Meta:
    model = Interest
    fields = "__all__"
