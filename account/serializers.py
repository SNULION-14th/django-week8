from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Teacher, Parent, Student

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  username = serializers.CharField()

  class Meta:
    model = User
    fields = ["id", "username", "password", "name", "phone", "role"]
    read_only_fields = ["role"]

class TeacherSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = Teacher
    fields = ["user", "major", "bio", "career"]

  def create(self, validate_data):
    user_data = validate_data.pop('user')
    user_data['role'] = 'teacher'

    user = User.objects.create_user(**user_data)

    teacher = Teacher.objects.create(user=user, **validate_data)
  
    return teacher

class ParentSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = Parent
    fields = ["user", "relationship", "memo"]

  def create(self, validate_data):
    user_data = validate_data.pop('user')
    user_data['role'] = 'parent'

    user = User.objects.create_user(**user_data)

    parent = Parent.objects.create(user=user, **validate_data)

    return parent

class StudentSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  parent = serializers.PrimaryKeyRelatedField(
    queryset=Parent.objects.all(),
    required=False,
    allow_null=True
  )

  class Meta:
    model = Student
    fields = ["user", "parent", "age", "school", "goal"]

  def create(self, validate_data):
    user_data = validate_data.pop('user')
    user_data['role'] = 'student'

    parent = validate_data.pop('parent', None)

    user = User.objects.create_user(**user_data)

    student = Student.objects.create(user=user, parent=parent, **validate_data)

    return student

class SignInRequestSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()