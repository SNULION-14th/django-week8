from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    # 비밀번호는 쓰기 전용으로 설정 (조회 시 노출 방지)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'age', 'major']

    def create(self, validated_data):
        # 유저를 생성할 때 비밀번호를 반드시 암호화해서 저장해야 로그인 가능!
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            age=validated_data.get('age'),   
            major=validated_data.get('major')
        )
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)