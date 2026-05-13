
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Post, Book
from .serializers import PostSerializer, BookSerializer

class PostListView(APIView):
    @extend_schema(summary="게시글 목록 조회", responses={200: PostSerializer(many=True)})
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @extend_schema(summary="게시글 생성", request=PostSerializer, responses={201: PostSerializer})
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    @extend_schema(
        summary="게시글 상세 조회",
        description="특정 ID의 게시글을 상세 조회합니다.",
        responses={200: PostSerializer, 404: "Not Found"}
    )
    def get(self, request, post_id):
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="게시글 수정",
        description="특정 ID의 게시글 정보를 일부 또는 전체 수정합니다.",
        request=PostSerializer,
        responses={200: PostSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, post_id):
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # partial=True 옵션으로 일부 필드만 수정(PATCH의 역할)이 가능하도록 설정
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="게시글 삭제",
        description="특정 ID의 게시글을 삭제합니다.",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




class BookListView(APIView):
    @extend_schema(
        tags=['Book'],
        summary="도서 목록 조회", 
        description="서비스에 등록된 모든 도서 목록을 조회합니다.", 
        responses={200: BookSerializer(many=True)}
    )
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Book'],
        summary="도서 등록", 
        description="새로운 도서 정보(ISBN, 제목, 저자 등)를 등록합니다.", 
        request=BookSerializer, 
        responses={201: BookSerializer}
    )
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailView(APIView):
    @extend_schema(tags=['Book'], summary="도서 상세 조회", responses={200: BookSerializer})
    def get(self, request, book_id):
        try:
            book = Book.objects.get(book_id=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Book'], summary="도서 정보 수정", request=BookSerializer, responses={200: BookSerializer})
    def put(self, request, book_id):
        try:
            book = Book.objects.get(book_id=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="도서 삭제", responses={204: "No Content"})
    def delete(self, request, book_id):
        try:
            book = Book.objects.get(book_id=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)