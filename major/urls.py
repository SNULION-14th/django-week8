# major/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MajorViewSet,
    UserViewSet,
    LectureViewSet,
    PreRequisiteRelationViewSet,
    CourseHistoryViewSet,
)

router = DefaultRouter()
router.register(r"majors", MajorViewSet)
router.register(r"users", UserViewSet)
router.register(r"lectures", LectureViewSet)
router.register(r"prerequisites", PreRequisiteRelationViewSet)
router.register(r"coursehistories", CourseHistoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
