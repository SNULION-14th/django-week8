from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, TeacherSerializer, ParentSerializer, StudentSerializer, SignInRequestSerializer
from drf_spectacular.utils import extend_schema

User = get_user_model()

class TeacherSignUpView(APIView):
  @extend_schema(
    summary="선생님 회원가입",
    description="선생님 회원가입을 진행합니다.",
    request=TeacherSerializer,
    responses={201: TeacherSerializer, 400: "Bad Request"},
  )
  def post(self, request):
    teacher_serializer = TeacherSerializer(data=request.data)

    if teacher_serializer.is_valid(raise_exception=True):
      teacher_serializer.save() # calls custom create() defined in TeacherSerializer
      return Response(teacher_serializer.data, status=status.HTTP_201_CREATED)

    return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParentSignUpView(APIView):
  @extend_schema(
    summary="학부모 회원가입",
    description="학부모 회원가입을 진행합니다.",
    request=ParentSerializer,
    responses={201: ParentSerializer, 400: "Bad Request"},
  )
  def post(self, request):
    parent_serializer = ParentSerializer(data=request.data)

    if parent_serializer.is_valid(raise_exception=True):
      parent_serializer.save()
      return Response(parent_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(parent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentSignUpView(APIView):
  @extend_schema(
    summary="학생 회원가입",
    description="학생 회원가입을 진행합니다.",
    request=StudentSerializer,
    responses={201: StudentSerializer, 400: "Bad Request"},
  )
  def post(self, request):
    student_serializer = StudentSerializer(data=request.data)

    if student_serializer.is_valid(raise_exception=True):
      student_serializer.save()
      return Response(student_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
  @extend_schema(
    summary="로그인",
    description="로그인을 진행합니다.",
    request=SignInRequestSerializer,
    responses={200: UserSerializer, 404: "Not Found", 400: "Bad Request"},
  )
  def post(self, request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
      return Response(
        {"message": "missing fields ['username', 'password'] in body"},
        status=status.HTTP_400_BAD_REQUEST,
      )
    try:
      user = User.objects.get(username=username)
      if not user.check_password(password):
        return Response(
          {"message": "Password is incorrect"},
          status=status.HTTP_400_BAD_REQUEST,
        )
      user_serializer = UserSerializer(user)
      return Response(user_serializer.data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
      return Response(
        {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
      )