from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer


@extend_schema_view(
    get=extend_schema(summary="프로필 목록 조회", responses={200: ProfileSerializer(many=True)}),
    post=extend_schema(summary="프로필 생성", request=ProfileSerializer, responses={201: ProfileSerializer}),
)
class ProfileListView(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.select_related('user')


@extend_schema_view(
    get=extend_schema(summary="프로필 상세 조회", responses={200: ProfileSerializer}),
    put=extend_schema(summary="프로필 수정", request=ProfileSerializer, responses={200: ProfileSerializer}),
    patch=extend_schema(summary="프로필 부분 수정", request=ProfileSerializer, responses={200: ProfileSerializer}),
    delete=extend_schema(summary="프로필 삭제", responses={204: OpenApiResponse(description="삭제 완료")}),
)
class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    lookup_field = 'profile_id'
    lookup_url_kwarg = 'profile_id'

    def get_queryset(self):
        return Profile.objects.select_related('user')
