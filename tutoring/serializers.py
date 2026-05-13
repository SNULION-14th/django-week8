from rest_framework.serializers import ModelSerializer
from .models import ClassInfo, ClassLog

class ClassInfoSerializer(ModelSerializer):
  class Meta:
    model = ClassInfo
    fields = "__all__"
    read_only_fields = ['teacher']

class ClassLogSerializer(ModelSerializer):
  class Meta:
    model = ClassLog
    fields = "__all__"
    read_only_fields = ['class_info']
