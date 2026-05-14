from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tag
from .serializers import TagSerializer

from post.models import Post
from post.serializers import PostSerializer
from seminar.serializers import DetailResponseSerializer


class TagListView(APIView):
  @extend_schema(
    summary='태그 목록 조회',
    description='태그 목록을 조회합니다.',
    responses={200: TagSerializer(many=True)}
  )
  def get(self, request):
    tags = Tag.objects.all()
    serializer = TagSerializer(instance=tags, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @extend_schema(
    summary='태그 생성',
    description='태그를 생성합니다.',
    request=TagSerializer,
    responses={201: TagSerializer, 400: DetailResponseSerializer, 409: DetailResponseSerializer}
  )
  def post(self, request):
    content = request.data.get('content')

    if not content:
      return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)

    if Tag.objects.filter(content=content).exists():
      return Response({"detail" : "Tag with same content already exists"}, status=status.HTTP_409_CONFLICT)

    tag = Tag.objects.create(content=content)
    serializer = TagSerializer(instance = tag)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagDetailView(APIView):
  @extend_schema(
    operation_id='tag_posts_list',
    summary='태그 내부 게시물 조회',
    description='해당 태그가 달린 게시물을 조회합니다.',
    responses={200: PostSerializer(many=True), 404: OpenApiResponse(description="Not Found")}
  )
  def get(self, request, tag_id):
    get_object_or_404(Tag, id=tag_id)

    posts = (
      Post.objects.select_related("author")
      .prefetch_related("tags", "comments", "like_users")
      .filter(tags=tag_id)
      .order_by("-created_at")
    )
    serializer = PostSerializer(instance=posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
