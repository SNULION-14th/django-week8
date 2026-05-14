from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from account.request_serializers import SignInRequestSerializer

from .serializers import UserSerializer

User = get_user_model()


class SignUpView(APIView):
    @extend_schema(
        summary="회원가입",
        description="회원가입을 진행합니다.",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class SignInView(APIView):
    @extend_schema(
        summary="로그인",
        description="로그인을 진행합니다.",
        request=SignInRequestSerializer,
        responses={
            200: UserSerializer,
            404: OpenApiResponse(description="Not Found"),
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    def post(self, request):
        request_serializer = SignInRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        username = request_serializer.validated_data["username"]
        password = request_serializer.validated_data["password"]

        user = get_object_or_404(User, username=username)
        if not user.check_password(password):
            return Response(
                {"message": "Password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
