from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Fixed_schedule
from drf_spectacular.utils import extend_schema

from account.request_serializers import SignInRequestSerializer, SignUpRequestSerializer
from .serializers import UserSerializer, FixedScheduleSerializer

User = get_user_model()

class SignUpView(APIView):
    @extend_schema(
        summary="회원가입",
        description="회원가입을 진행합니다.",
        request=SignUpRequestSerializer,
        responses={201: UserSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            user.set_password(request.data.get("password"))
            user.save()

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


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
        
class FixedScheduleView(APIView):
  @extend_schema(
      summary="고정 일정 등록",
      description="이름과 시간 등을 입력받아 새로운 고정 일정을 등록합니다.",
      request=FixedScheduleSerializer,
      responses={201: FixedScheduleSerializer}
    )
  def post(self, request):
    title = request.data.get('title')
    start_time = request.data.get('start_time')
    end_time = request.data.get('end_time')
    if not title or not start_time or not end_time :
      return Response({"detail": "[title, start_time, end_time] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
    fixed_schedule = Fixed_schedule.objects.create(
                            title=title, 
                            start_time=start_time,
                            end_time=end_time)
    serializer = FixedScheduleSerializer(fixed_schedule)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class FixedScheduleSingleView(APIView):
  @extend_schema(
        summary="고정 일정 상세 조회",
        description="고정 일정 1개의 상세 정보를 조회합니다.",
        responses={200: FixedScheduleSerializer}
    )
  def get(self, request, schedule_id):
    try:
      task = Fixed_schedule.objects.get(id=schedule_id)
    except:
      return Response({"single": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = FixedScheduleSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @extend_schema(
        summary="고정 일정 삭제",
        description="고정 일정을 삭제합니다.",
        responses={204: None}
    )
  def delete(self, request, schedule_id):
    try:
      fixed_schedule =  Fixed_schedule.objects.get(id=schedule_id)
    except:
      return Response({"single": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    fixed_schedule.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)