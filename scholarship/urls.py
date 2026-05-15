from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScholarshipViewSet, SchoolViewSet

router = DefaultRouter()
router.register("scholarships", ScholarshipViewSet)
router.register("schools", ScholarshipViewSet, basename="school")

urlpatterns = [
    path("", include(router.urls)),
]