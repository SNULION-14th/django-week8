from django.urls import path, include
from .views import ClassInfoViewSet, ClassLogViewSet

app_name = 'tutoring'

urlpatterns = [
  # CBV url path

  # ClassInfo 관련 url
  path("", ClassInfoViewSet.as_view({
    'get': 'list',
    'post': 'create'
  })),
  path("<int:pk>/", ClassInfoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
  })),

  # ClassLog 관련 url
  path("<int:class_info_id>/logs/", ClassLogViewSet.as_view({
    'get': 'list',
    'post': 'create'
  })),
  path("<int:class_info_id>/logs/<int:pk>/", ClassLogViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
  })),
]