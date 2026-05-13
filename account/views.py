from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Profile
from .serializers import ProfileSerializer

class ProfileListView(APIView):
    @extend_schema(summary="프로필 목록 조회", description="모든 유저의 프로필을 조회합니다.", responses={200: ProfileSerializer(many=True)})
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="프로필 생성", description="새로운 프로필을 생성합니다.", request=ProfileSerializer, responses={201: ProfileSerializer})
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailView(APIView):
    @extend_schema(summary="프로필 상세 조회", responses={200: ProfileSerializer})
    def get(self, request, profile_id):
        try:
            profile = Profile.objects.get(profile_id=profile_id)
        except Profile.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="프로필 수정", request=ProfileSerializer, responses={200: ProfileSerializer})
    def put(self, request, profile_id):
        try:
            profile = Profile.objects.get(profile_id=profile_id)
        except Profile.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="프로필 삭제", responses={204: "No Content"})
    def delete(self, request, profile_id):
        try:
            profile = Profile.objects.get(profile_id=profile_id)
        except Profile.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)