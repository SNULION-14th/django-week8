# ./account/serializers.py

from rest_framework import serializers # 명칭 통일
from django.contrib.auth import get_user_model

User = get_user_model()

# 1. 다른 모델(진단 리포트 등)에서 "참조용"으로 쓸 가벼운 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "college", "major"]

# 2. 회원가입이나 로그인 시 "입력용"으로 쓸 시리얼라이저
class UserJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "college", "major"]
        extra_kwargs = {'password': {'write_only': True}}