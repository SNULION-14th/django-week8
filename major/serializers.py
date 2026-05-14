from rest_framework import serializers
from .models import (
    Student,
    Department,
    Course,
    Interest,
    StudentInterest,
    DepartmentInterest,
    Recommendation,
)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'


class StudentInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInterest
        fields = '__all__'


class DepartmentInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentInterest
        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'