from django.urls import path
# 추가
from .views import (
    PostListView, PostDetailView,
    LogListAPIView, LogDetailAPIView,
)

app_name = 'post'

# api/post/로 시작하는 url은 이곳으로 왔다.
# 그 이후에 붙는 것부터 여기서 찾는 것이다.
# 예) api/post/3이라면 <int:post_id>로
urlpatterns = [
    # ── Post ──
    path("", PostListView.as_view()),
    path("<int:post_id>/", PostDetailView.as_view()),

    # ── Log ──
    path("logs/", LogListAPIView.as_view(), name='log-list'),
    path("logs/<int:pk>/", LogDetailAPIView.as_view(), name='log-detail'),
]