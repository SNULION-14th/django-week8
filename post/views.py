
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import generics
from .models import Post, Book
from .serializers import PostSerializer, BookSerializer


@extend_schema_view(
    get=extend_schema(summary="게시글 목록 조회", responses={200: PostSerializer(many=True)}),
    post=extend_schema(summary="게시글 생성", request=PostSerializer, responses={201: PostSerializer}),
)
class PostListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.select_related('user', 'book')


@extend_schema_view(
    get=extend_schema(summary="게시글 상세 조회", responses={200: PostSerializer}),
    put=extend_schema(summary="게시글 수정", request=PostSerializer, responses={200: PostSerializer}),
    patch=extend_schema(summary="게시글 부분 수정", request=PostSerializer, responses={200: PostSerializer}),
    delete=extend_schema(summary="게시글 삭제", responses={204: OpenApiResponse(description="삭제 완료")}),
)
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    lookup_field = 'post_id'
    lookup_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.select_related('user', 'book')


@extend_schema_view(
    get=extend_schema(tags=['Book'], summary="도서 목록 조회", responses={200: BookSerializer(many=True)}),
    post=extend_schema(tags=['Book'], summary="도서 등록", request=BookSerializer, responses={201: BookSerializer}),
)
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


@extend_schema_view(
    get=extend_schema(tags=['Book'], summary="도서 상세 조회", responses={200: BookSerializer}),
    put=extend_schema(tags=['Book'], summary="도서 정보 수정", request=BookSerializer, responses={200: BookSerializer}),
    patch=extend_schema(tags=['Book'], summary="도서 정보 부분 수정", request=BookSerializer, responses={200: BookSerializer}),
    delete=extend_schema(tags=['Book'], summary="도서 삭제", responses={204: OpenApiResponse(description="삭제 완료")}),
)
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'book_id'
    lookup_url_kwarg = 'book_id'
