from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    GatchaDrawViewSet,
    GatchaItemViewSet,
    GatchaPoolItemViewSet,
    GatchaTypeViewSet,
    UserViewSet,
)

app_name = "gatcha"

router = DefaultRouter()
router.register("users", UserViewSet, basename="gatcha-user")
router.register("types", GatchaTypeViewSet, basename="gatcha-type")
router.register("items", GatchaItemViewSet, basename="gatcha-item")
router.register("pool-items", GatchaPoolItemViewSet, basename="gatcha-pool-item")
router.register("draw", GatchaDrawViewSet, basename="gatcha-draw")

urlpatterns = [
    path("", include(router.urls)),
]
