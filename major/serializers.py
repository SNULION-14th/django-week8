# major/serializers.py

from rest_framework import serializers
from .models import Major, User, Lecture, PreRequisiteRelation, CourseHistory


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = "__all__"


class PreRequisiteRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreRequisiteRelation
        fields = "__all__"


class CourseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseHistory
        fields = "__all__"
