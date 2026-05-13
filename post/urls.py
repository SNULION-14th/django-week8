from django.urls import path
from .views import PostListView, PostDetailView, BookListView, BookDetailView

app_name = 'post'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('book/', BookListView.as_view(), name='book-list'),
    path('book/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
]