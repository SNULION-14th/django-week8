from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from .serializers import SignupSerializer, LoginSerializer 

# 1. 회원가입 View
class SignupView(APIView):
    permission_classes = [AllowAny] # 누구나 접근 가능
    serializer_class = SignupSerializer

    @extend_schema(
        summary="회원가입",
        description="새로운 유저를 생성합니다.",
        request=SignupSerializer,
        responses={201: SignupSerializer}
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(SignupSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. 로그인 View
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        summary="로그인",
        description="아이디와 비밀번호로 로그인합니다.",
        request=LoginSerializer, # 로그인에 필요한 필드만 담긴 Serializer 권장
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# 3. 로그아웃 View
@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated] # 로그인한 사람만 가능
    serializer_class = LoginSerializer

    @extend_schema(summary="로그아웃")
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

# 4. 내 프로필 정보 View
class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginSerializer

    @extend_schema(
        summary="내 프로필 조회",
        responses={200: LoginSerializer}
    )
    def get(self, request):
        # request.user를 통해 현재 로그인된 유저 정보를 가져옴
        serializer = LoginSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)