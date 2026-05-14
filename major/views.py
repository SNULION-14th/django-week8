from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import generics

from .models import (
    Course,
    Department,
    DepartmentInterest,
    Interest,
    Recommendation,
    Student,
    StudentInterest,
)
from .serializers import (
    CourseSerializer,
    DepartmentInterestSerializer,
    DepartmentSerializer,
    InterestSerializer,
    RecommendationSerializer,
    StudentInterestSerializer,
    StudentSerializer,
)


@extend_schema_view(
    get=extend_schema(summary='학생 목록 조회', responses={200: StudentSerializer(many=True)}),
    post=extend_schema(summary='학생 생성', request=StudentSerializer, responses={201: StudentSerializer}),
)
class StudentListView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


@extend_schema_view(
    get=extend_schema(summary='학생 상세 조회', responses={200: StudentSerializer}),
    put=extend_schema(summary='학생 수정', request=StudentSerializer, responses={200: StudentSerializer}),
    patch=extend_schema(summary='학생 부분 수정', request=StudentSerializer, responses={200: StudentSerializer}),
    delete=extend_schema(summary='학생 삭제', responses={204: OpenApiResponse(description='삭제 성공')}),
)
class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_url_kwarg = 'student_id'


@extend_schema_view(
    get=extend_schema(summary='학과 목록 조회', responses={200: DepartmentSerializer(many=True)}),
    post=extend_schema(summary='학과 생성', request=DepartmentSerializer, responses={201: DepartmentSerializer}),
)
class DepartmentListView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


@extend_schema_view(
    get=extend_schema(summary='학과 상세 조회', responses={200: DepartmentSerializer}),
    put=extend_schema(summary='학과 수정', request=DepartmentSerializer, responses={200: DepartmentSerializer}),
    patch=extend_schema(summary='학과 부분 수정', request=DepartmentSerializer, responses={200: DepartmentSerializer}),
    delete=extend_schema(summary='학과 삭제', responses={204: OpenApiResponse(description='삭제 성공')}),
)
class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_url_kwarg = 'department_id'


@extend_schema_view(
    get=extend_schema(summary='수업 목록 조회', responses={200: CourseSerializer(many=True)}),
    post=extend_schema(summary='수업 생성', request=CourseSerializer, responses={201: CourseSerializer}),
)
class CourseListView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.select_related('department')


@extend_schema_view(
    get=extend_schema(summary='수업 상세 조회', responses={200: CourseSerializer}),
    put=extend_schema(summary='수업 수정', request=CourseSerializer, responses={200: CourseSerializer}),
    patch=extend_schema(summary='수업 부분 수정', request=CourseSerializer, responses={200: CourseSerializer}),
    delete=extend_schema(summary='수업 삭제', responses={204: OpenApiResponse(description='삭제 성공')}),
)
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    lookup_url_kwarg = 'course_id'

    def get_queryset(self):
        return Course.objects.select_related('department')


@extend_schema_view(
    get=extend_schema(summary='관심사 목록 조회', responses={200: InterestSerializer(many=True)}),
    post=extend_schema(summary='관심사 생성', request=InterestSerializer, responses={201: InterestSerializer}),
)
class InterestListView(generics.ListCreateAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer


@extend_schema_view(
    get=extend_schema(summary='관심사 상세 조회', responses={200: InterestSerializer}),
    put=extend_schema(summary='관심사 수정', request=InterestSerializer, responses={200: InterestSerializer}),
    patch=extend_schema(summary='관심사 부분 수정', request=InterestSerializer, responses={200: InterestSerializer}),
    delete=extend_schema(summary='관심사 삭제', responses={204: OpenApiResponse(description='삭제 성공')}),
)
class InterestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    lookup_url_kwarg = 'interest_id'


@extend_schema_view(
    get=extend_schema(summary='학생 관심사 목록 조회', responses={200: StudentInterestSerializer(many=True)}),
    post=extend_schema(summary='학생 관심사 생성', request=StudentInterestSerializer, responses={201: StudentInterestSerializer}),
)
class StudentInterestListView(generics.ListCreateAPIView):
    serializer_class = StudentInterestSerializer

    def get_queryset(self):
        return StudentInterest.objects.select_related('student', 'interest')


@extend_schema_view(
    get=extend_schema(summary='학생 관심사 상세 조회', responses={200: StudentInterestSerializer}),
    put=extend_schema(summary='학생 관심사 수정', request=StudentInterestSerializer, responses={200: StudentInterestSerializer}),
    patch=extend_schema(summary='학생 관심사 부분 수정', request=StudentInterestSerializer, responses={200: StudentInterestSerializer}),
    delete=extend_schema(summary='학생 관심사 삭제', responses={204: OpenApiResponse(description='삭제 성공')}),
)
class StudentInterestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentInterestSerializer
    lookup_url_kwarg = 'student_interest_id'

    def get_queryset(self):
        return StudentInterest.objects.select_related('student', 'interest')


@extend_schema_view(
    get=extend_schema(summary='학과 관심사 목록 조회', responses={200: DepartmentInterestSerializer(many=True)}),
    post=extend_schema(summary='학과 관심사 생성', request=DepartmentInterestSerializer, responses={201: DepartmentInterestSerializer}),
)
class DepartmentInterestListView(generics.ListCreateAPIView):
    serializer_class = DepartmentInterestSerializer

    def get_queryset(self):
        return DepartmentInterest.objects.select_related('department', 'interest')


@extend_schema_view(
    get=extend_schema(summary='학과 관심사 상세 조회', responses={200: DepartmentInterestSerializer}),
    put=extend_schema(summary='학과 관심사 수정', request=DepartmentInterestSerializer, responses={200: DepartmentInterestSerializer}),
    patch=extend_schema(summary='학과 관심사 부분 수정', request=DepartmentInterestSerializer, responses={200: DepartmentInterestSerializer}),
    delete=extend_schema(summary='학과 관심사 삭제', responses={204: OpenApiResponse(description='삭제 성공')}),
)
class DepartmentInterestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DepartmentInterestSerializer
    lookup_url_kwarg = 'department_interest_id'

    def get_queryset(self):
        return DepartmentInterest.objects.select_related('department', 'interest')


@extend_schema_view(
    get=extend_schema(summary='추천 결과 목록 조회', responses={200: RecommendationSerializer(many=True)}),
    post=extend_schema(summary='추천 결과 생성', request=RecommendationSerializer, responses={201: RecommendationSerializer}),
)
class RecommendationListView(generics.ListCreateAPIView):
    serializer_class = RecommendationSerializer

    def get_queryset(self):
        return Recommendation.objects.select_related('student', 'department')


@extend_schema_view(
    get=extend_schema(summary='추천 결과 상세 조회', responses={200: RecommendationSerializer}),
    put=extend_schema(summary='추천 결과 수정', request=RecommendationSerializer, responses={200: RecommendationSerializer}),
    patch=extend_schema(summary='추천 결과 부분 수정', request=RecommendationSerializer, responses={200: RecommendationSerializer}),
    delete=extend_schema(summary='추천 결과 삭제', responses={204: OpenApiResponse(description='삭제 성공')}),
)
class RecommendationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecommendationSerializer
    lookup_url_kwarg = 'recommendation_id'

    def get_queryset(self):
        return Recommendation.objects.select_related('student', 'department')
