# ./post/urls.py

from django.urls import path
# 추가
from .views import (
  UserProfileListView, UserProfileDetailView,
  StockListView, StockDetailView,
  RecommendationListView, RecommendationDetailView,
  ReasonListView, ReasonDetailView,
  BookmarkListView, BookmarkDetailView
)

app_name = 'stock'

urlpatterns = [
    # CBV url path
    path("users", UserProfileListView.as_view()),
    path("users/<str:pk>/", UserProfileDetailView.as_view()),
    path("stocks", StockListView.as_view()),
    path("stocks/<str:pk>/", StockDetailView.as_view()),
    path("recommendations", RecommendationListView.as_view()),
    path("recommendations/<str:pk>/", RecommendationDetailView.as_view()),
    path("reasons", ReasonListView.as_view()),
    path("reasons/<str:pk>/", ReasonDetailView.as_view()),
    path("bookmarks", BookmarkListView.as_view()),
    path("bookmarks/<str:pk>/", BookmarkDetailView.as_view()),
]