from django.urls import path

from .views import (
    CommentDetailView,
    CommentListView,
    LikeView,
    PostDetailView,
    PostListView,
)

app_name = "post"

urlpatterns = [
    path("", PostListView.as_view()),
    path("<int:post_id>/", PostDetailView.as_view()),
    path("<int:post_id>/comment/", CommentListView.as_view()),
    path("comment/<int:comment_id>/", CommentDetailView.as_view()),
    path("<int:post_id>/like/", LikeView.as_view()),
]
