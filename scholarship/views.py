from django.shortcuts import render

# Create your views here.
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet
from .models import Scholarship, School
from .serializers import ScholarshipSerializer, SchoolSerializer

@extend_schema(
    tags=["Scholarship"],
    summary="장학금 CRUD API",
    description="장학금 정보를 조회, 생성, 수정, 삭제할 수 있는 API입니다.",
)
class ScholarshipViewSet(ModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer

@extend_schema(
    tags=["School"],
    summary="학교 CRUD API",
    description="학교 정보를 조회, 생성, 수정, 삭제할 수 있는 API입니다.",
)
class SchoolViewSet(ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer