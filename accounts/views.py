from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from utils.auth import authorize_user
from .models import Interest
from .serializers import UserSerializer, InterestSerializer
from .request_serializers import SignInRequestSerializer, SignUpRequestSerializer, InterestListRequestSerializer, InterestDetailRequestSerializer

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


class InterestListView(APIView):
  @extend_schema(
    summary="관심사 목록 조회",
    description="관심사 목록을 조회합니다.",
    responses={
      200: InterestSerializer(many=True),
      404: "Not Found",
      400: "Bad Request",
    },
  )
  def get(self, request, user_id):
    interests = User.objects.get(id=user_id).interests.all()
    serializer = InterestSerializer(interests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @extend_schema(
    summary="관심사 생성",
    description="관심사를 생성합니다.",
    request=InterestListRequestSerializer,
    responses={
      201: InterestSerializer,
      404: "Not Found",
      400: "Bad Request"
    },
  )
  def post(self, request, user_id):
    user_info = request.data.get("user")
    keyword = request.data.get("keyword")
    description = request.data.get("description")
    priority = request.data.get("priority")

    auth = authorize_user(User, user_info)
    if not auth.is_auth:
      return auth.response
    if user_id != auth.user.id:
      return Response(
        {"detail": "User unmatched"},
        status=status.HTTP_400_BAD_REQUEST,
      )
    
    if not (keyword and description and (priority != None)):
      return Response(
        {"detail": "[keyword, description, priority] fields missing."},
        status=status.HTTP_400_BAD_REQUEST,
      )
    
    interest = Interest.objects.create(user=auth.user, keyword=keyword, description=description, priority=priority)

    serializer = InterestSerializer(interest)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class InterestDetailView(APIView):
  @extend_schema(
    summary="관심사 상세 조회",
    description="관심사 1개의 상세 정보를 조회합니다.",
    responses={
      200: InterestSerializer,
      400: "Bad Request"
    },
  )
  def get(self, request, user_id, interest_id):
      try:
        interest = User.objects.get(id=user_id).interests.get(id=interest_id)
      except:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

      serializer = InterestSerializer(instance=interest)

      return Response(serializer.data, status=status.HTTP_200_OK)
  
  @extend_schema(
    summary="관심사 삭제",
    description="관심사를 삭제합니다.",
    responses={
      204: "No Content",
      404: "Not Found",
      400: "Bad Request"
    },
  )
  def delete(self, request, user_id, interest_id):
    try:
      interest = User.objects.get(id=user_id).interests.get(id=interest_id)
    except:
      return Response(
        {"detail": "Interest Not found."}, status=status.HTTP_404_NOT_FOUND
      )

    interest.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  @extend_schema(
      summary="관심사 수정",
      description="관심사를 수정합니다.",
      request=InterestDetailRequestSerializer,
      responses={
        200: InterestSerializer,
        404: "Not Found",
        400: "Bad Request"
      },
  )
  def put(self, request, user_id, interest_id):
    try:
      interest = User.objects.get(id=user_id).interests.get(id=interest_id)
    except:
      return Response(
        {"detail": "Interest not found."}, status=status.HTTP_404_NOT_FOUND
      )

    user_info = request.data.get("user")
    keyword = request.data.get("keyword")
    description = request.data.get("description")
    priority = request.data.get("priority")

    auth = authorize_user(User, user_info)
    if not auth.is_auth:
      return auth.response
    if interest.user != auth.user:
      return Response(
        {"detail": "You are not the user of this interest."},
        status=status.HTTP_403_FORBIDDEN,
      )
    
    if not (keyword and description and (priority != None)):
      return Response(
        {"detail": "[keyword, description, priority] fields missing."},
        status=status.HTTP_400_BAD_REQUEST,
      )
    interest.keyword = keyword
    interest.description = description
    interest.priority = priority

    interest.save()
    serializer = InterestSerializer(instance=interest)
    return Response(serializer.data, status=status.HTTP_200_OK)
