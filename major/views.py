# major/views.py

from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from .models import Major, User, Lecture, PreRequisiteRelation, CourseHistory
from .serializers import (
    MajorSerializer,
    UserSerializer,
    LectureSerializer,
    PreRequisiteRelationSerializer,
    CourseHistorySerializer,
)


class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer


class PreRequisiteRelationViewSet(viewsets.ModelViewSet):
    queryset = PreRequisiteRelation.objects.all()
    serializer_class = PreRequisiteRelationSerializer


class CourseHistoryViewSet(viewsets.ModelViewSet):
    queryset = CourseHistory.objects.all()
    serializer_class = CourseHistorySerializer
