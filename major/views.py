from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .models import (
    Student,
    Department,
    Course,
    Interest,
    StudentInterest,
    DepartmentInterest,
    Recommendation,
)

from .serializers import (
    StudentSerializer,
    DepartmentSerializer,
    CourseSerializer,
    InterestSerializer,
    StudentInterestSerializer,
    DepartmentInterestSerializer,
    RecommendationSerializer,
)


class StudentListView(APIView):
    @extend_schema(
        summary='학생 목록 조회',
        description='등록된 모든 학생 목록을 조회합니다.',
        responses={200: StudentSerializer(many=True)}
    )
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(instance=students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='학생 생성',
        description='새로운 학생 정보를 생성합니다.',
        request=StudentSerializer,
        responses={201: StudentSerializer, 400: {'description': '잘못된 요청'}}
    )
    def post(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    @extend_schema(
        summary='학생 상세 조회',
        description='student_id에 해당하는 학생 정보를 조회합니다.',
        responses={200: StudentSerializer, 404: {'description': '학생을 찾을 수 없음'}}
    )
    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response(
                {"detail": "해당 학생이 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(instance=student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='학생 삭제',
        description='student_id에 해당하는 학생 정보를 삭제합니다.',
        responses={204: {'description': '삭제 성공'}, 404: {'description': '학생을 찾을 수 없음'}}
    )
    def delete(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response(
                {"detail": "해당 학생이 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DepartmentListView(APIView):
    @extend_schema(
        summary='학과 목록 조회',
        description='등록된 모든 학과 목록을 조회합니다.',
        responses={200: DepartmentSerializer(many=True)}
    )
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(instance=departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='학과 생성',
        description='새로운 학과를 생성합니다.',
        request=DepartmentSerializer,
        responses={201: DepartmentSerializer, 400: {'description': '잘못된 요청'}}
    )
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetailView(APIView):
    @extend_schema(
        summary='학과 상세 조회',
        description='department_id에 해당하는 학과 정보를 조회합니다.',
        responses={200: DepartmentSerializer, 404: {'description': '학과를 찾을 수 없음'}}
    )
    def get(self, request, department_id):
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response(
                {"detail": "해당 학과가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DepartmentSerializer(instance=department)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='학과 삭제',
        description='department_id에 해당하는 학과를 삭제합니다.',
        responses={204: {'description': '삭제 성공'}, 404: {'description': '학과를 찾을 수 없음'}}
    )
    def delete(self, request, department_id):
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response(
                {"detail": "해당 학과가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class CourseListView(APIView):
    @extend_schema(
        summary='수업 목록 조회',
        description='등록된 모든 전공 수업 목록을 조회합니다.',
        responses={200: CourseSerializer(many=True)}
    )
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(instance=courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='수업 생성',
        description='새로운 전공 수업을 생성합니다.',
        request=CourseSerializer,
        responses={201: CourseSerializer, 400: {'description': '잘못된 요청'}}
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    @extend_schema(
        summary='수업 상세 조회',
        description='course_id에 해당하는 전공 수업 정보를 조회합니다.',
        responses={200: CourseSerializer, 404: {'description': '수업을 찾을 수 없음'}}
    )
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"detail": "해당 수업이 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CourseSerializer(instance=course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='수업 삭제',
        description='course_id에 해당하는 전공 수업을 삭제합니다.',
        responses={204: {'description': '삭제 성공'}, 404: {'description': '수업을 찾을 수 없음'}}
    )
    def delete(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"detail": "해당 수업이 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class InterestListView(APIView):
    @extend_schema(
        summary='관심사 목록 조회',
        description='등록된 모든 관심사 목록을 조회합니다.',
        responses={200: InterestSerializer(many=True)}
    )
    def get(self, request):
        interests = Interest.objects.all()
        serializer = InterestSerializer(instance=interests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='관심사 생성',
        description='새로운 관심사를 생성합니다.',
        request=InterestSerializer,
        responses={201: InterestSerializer, 400: {'description': '잘못된 요청'}}
    )
    def post(self, request):
        serializer = InterestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InterestDetailView(APIView):
    @extend_schema(
        summary='관심사 상세 조회',
        description='interest_id에 해당하는 관심사 정보를 조회합니다.',
        responses={200: InterestSerializer, 404: {'description': '관심사를 찾을 수 없음'}}
    )
    def get(self, request, interest_id):
        try:
            interest = Interest.objects.get(id=interest_id)
        except Interest.DoesNotExist:
            return Response(
                {"detail": "해당 관심사가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InterestSerializer(instance=interest)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='관심사 삭제',
        description='interest_id에 해당하는 관심사를 삭제합니다.',
        responses={204: {'description': '삭제 성공'}, 404: {'description': '관심사를 찾을 수 없음'}}
    )
    def delete(self, request, interest_id):
        try:
            interest = Interest.objects.get(id=interest_id)
        except Interest.DoesNotExist:
            return Response(
                {"detail": "해당 관심사가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        interest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class StudentInterestListView(APIView):
    @extend_schema(
        summary='학생 관심사 목록 조회',
        description='학생별 관심사와 선호도 목록을 조회합니다.',
        responses={200: StudentInterestSerializer(many=True)}
    )
    def get(self, request):
        student_interests = StudentInterest.objects.all()
        serializer = StudentInterestSerializer(instance=student_interests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='학생 관심사 생성',
        description='특정 학생의 관심사와 선호도를 생성합니다.',
        request=StudentInterestSerializer,
        responses={201: StudentInterestSerializer, 400: {'description': '잘못된 요청'}}
    )
    def post(self, request):
        serializer = StudentInterestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentInterestDetailView(APIView):
    @extend_schema(
        summary='학생 관심사 상세 조회',
        description='student_interest_id에 해당하는 학생 관심사 정보를 조회합니다.',
        responses={200: StudentInterestSerializer, 404: {'description': '학생 관심사를 찾을 수 없음'}}
    )
    def get(self, request, student_interest_id):
        try:
            student_interest = StudentInterest.objects.get(id=student_interest_id)
        except StudentInterest.DoesNotExist:
            return Response(
                {"detail": "해당 학생 관심사 정보가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentInterestSerializer(instance=student_interest)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='학생 관심사 삭제',
        description='student_interest_id에 해당하는 학생 관심사 정보를 삭제합니다.',
        responses={204: {'description': '삭제 성공'}, 404: {'description': '학생 관심사를 찾을 수 없음'}}
    )
    def delete(self, request, student_interest_id):
        try:
            student_interest = StudentInterest.objects.get(id=student_interest_id)
        except StudentInterest.DoesNotExist:
            return Response(
                {"detail": "해당 학생 관심사 정보가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        student_interest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DepartmentInterestListView(APIView):
    @extend_schema(
        summary='학과 관심사 목록 조회',
        description='학과별 관심 분야와 관련도 목록을 조회합니다.',
        responses={200: DepartmentInterestSerializer(many=True)}
    )
    def get(self, request):
        department_interests = DepartmentInterest.objects.all()
        serializer = DepartmentInterestSerializer(instance=department_interests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='학과 관심사 생성',
        description='특정 학과의 관심 분야와 관련도를 생성합니다.',
        request=DepartmentInterestSerializer,
        responses={201: DepartmentInterestSerializer, 400: {'description': '잘못된 요청'}}
    )
    def post(self, request):
        serializer = DepartmentInterestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentInterestDetailView(APIView):
    @extend_schema(
        summary='학과 관심사 상세 조회',
        description='department_interest_id에 해당하는 학과 관심사 정보를 조회합니다.',
        responses={200: DepartmentInterestSerializer, 404: {'description': '학과 관심사를 찾을 수 없음'}}
    )
    def get(self, request, department_interest_id):
        try:
            department_interest = DepartmentInterest.objects.get(id=department_interest_id)
        except DepartmentInterest.DoesNotExist:
            return Response(
                {"detail": "해당 학과 관심사 정보가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DepartmentInterestSerializer(instance=department_interest)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='학과 관심사 삭제',
        description='department_interest_id에 해당하는 학과 관심사 정보를 삭제합니다.',
        responses={204: {'description': '삭제 성공'}, 404: {'description': '학과 관심사를 찾을 수 없음'}}
    )
    def delete(self, request, department_interest_id):
        try:
            department_interest = DepartmentInterest.objects.get(id=department_interest_id)
        except DepartmentInterest.DoesNotExist:
            return Response(
                {"detail": "해당 학과 관심사 정보가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        department_interest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class RecommendationListView(APIView):
    @extend_schema(
        summary='추천 결과 목록 조회',
        description='학생에게 제공된 모든 학과 추천 결과를 조회합니다.',
        responses={200: RecommendationSerializer(many=True)}
    )
    def get(self, request):
        recommendations = Recommendation.objects.all()
        serializer = RecommendationSerializer(instance=recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='추천 결과 생성',
        description='학생에게 새로운 학과 추천 결과를 생성합니다.',
        request=RecommendationSerializer,
        responses={201: RecommendationSerializer, 400: {'description': '잘못된 요청'}}
    )
    def post(self, request):
        serializer = RecommendationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationDetailView(APIView):
    @extend_schema(
        summary='추천 결과 상세 조회',
        description='recommendation_id에 해당하는 추천 결과를 조회합니다.',
        responses={200: RecommendationSerializer, 404: {'description': '추천 결과를 찾을 수 없음'}}
    )
    def get(self, request, recommendation_id):
        try:
            recommendation = Recommendation.objects.get(id=recommendation_id)
        except Recommendation.DoesNotExist:
            return Response(
                {"detail": "해당 추천 결과가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RecommendationSerializer(instance=recommendation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='추천 결과 삭제',
        description='recommendation_id에 해당하는 추천 결과를 삭제합니다.',
        responses={204: {'description': '삭제 성공'}, 404: {'description': '추천 결과를 찾을 수 없음'}}
    )
    def delete(self, request, recommendation_id):
        try:
            recommendation = Recommendation.objects.get(id=recommendation_id)
        except Recommendation.DoesNotExist:
            return Response(
                {"detail": "해당 추천 결과가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        recommendation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)