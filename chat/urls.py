from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ChatRoomMemberViewSet,
    ChatRoomViewSet,
    LanguageViewSet,
    MessageTranslationViewSet,
    MessageViewSet,
    UserViewSet,
)

app_name = "chat"

router = DefaultRouter()
router.register("languages", LanguageViewSet, basename="language")
router.register("users", UserViewSet, basename="user")
router.register("rooms", ChatRoomViewSet, basename="chat-room")
router.register("members", ChatRoomMemberViewSet, basename="chat-room-member")
router.register("messages", MessageViewSet, basename="message")
router.register("translations", MessageTranslationViewSet, basename="message-translation")

urlpatterns = [
    path("", include(router.urls)),
]
