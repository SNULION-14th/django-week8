from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet

from .models import (
    ChatRoom,
    ChatRoomMember,
    Language,
    Message,
    MessageTranslation,
    User,
)
from .serializers import (
    ChatRoomMemberSerializer,
    ChatRoomSerializer,
    LanguageSerializer,
    MessageSerializer,
    MessageTranslationSerializer,
    UserSerializer,
)


@extend_schema_view(
    list=extend_schema(summary="지원 언어 목록 조회"),
    retrieve=extend_schema(summary="지원 언어 상세 조회"),
    create=extend_schema(summary="지원 언어 생성"),
    update=extend_schema(summary="지원 언어 전체 수정"),
    partial_update=extend_schema(summary="지원 언어 일부 수정"),
    destroy=extend_schema(summary="지원 언어 삭제"),
)
class LanguageViewSet(ModelViewSet):
    queryset = Language.objects.all().order_by("code")
    serializer_class = LanguageSerializer


@extend_schema_view(
    list=extend_schema(summary="채팅 사용자 목록 조회"),
    retrieve=extend_schema(summary="채팅 사용자 상세 조회"),
    create=extend_schema(summary="채팅 사용자 생성"),
    update=extend_schema(summary="채팅 사용자 전체 수정"),
    partial_update=extend_schema(summary="채팅 사용자 일부 수정"),
    destroy=extend_schema(summary="채팅 사용자 삭제"),
)
class UserViewSet(ModelViewSet):
    queryset = User.objects.select_related("preferred_language_code").all().order_by("id")
    serializer_class = UserSerializer


@extend_schema_view(
    list=extend_schema(summary="채팅방 목록 조회"),
    retrieve=extend_schema(summary="채팅방 상세 조회"),
    create=extend_schema(summary="채팅방 생성"),
    update=extend_schema(summary="채팅방 전체 수정"),
    partial_update=extend_schema(summary="채팅방 일부 수정"),
    destroy=extend_schema(summary="채팅방 삭제"),
)
class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.select_related("created_by").all().order_by("id")
    serializer_class = ChatRoomSerializer


@extend_schema_view(
    list=extend_schema(summary="채팅방 참여자 목록 조회"),
    retrieve=extend_schema(summary="채팅방 참여자 상세 조회"),
    create=extend_schema(summary="채팅방 참여자 생성"),
    update=extend_schema(summary="채팅방 참여자 전체 수정"),
    partial_update=extend_schema(summary="채팅방 참여자 일부 수정"),
    destroy=extend_schema(summary="채팅방 참여자 삭제"),
)
class ChatRoomMemberViewSet(ModelViewSet):
    queryset = (
        ChatRoomMember.objects.select_related(
            "chat_room",
            "user",
            "display_language_code",
            "last_read_message",
        )
        .all()
        .order_by("id")
    )
    serializer_class = ChatRoomMemberSerializer


@extend_schema_view(
    list=extend_schema(summary="메시지 목록 조회"),
    retrieve=extend_schema(summary="메시지 상세 조회"),
    create=extend_schema(summary="메시지 생성"),
    update=extend_schema(summary="메시지 전체 수정"),
    partial_update=extend_schema(summary="메시지 일부 수정"),
    destroy=extend_schema(summary="메시지 삭제"),
)
class MessageViewSet(ModelViewSet):
    queryset = (
        Message.objects.select_related(
            "chat_room",
            "sender",
            "original_language_code",
        )
        .all()
        .order_by("id")
    )
    serializer_class = MessageSerializer


@extend_schema_view(
    list=extend_schema(summary="메시지 번역 목록 조회"),
    retrieve=extend_schema(summary="메시지 번역 상세 조회"),
    create=extend_schema(summary="메시지 번역 생성"),
    update=extend_schema(summary="메시지 번역 전체 수정"),
    partial_update=extend_schema(summary="메시지 번역 일부 수정"),
    destroy=extend_schema(summary="메시지 번역 삭제"),
)
class MessageTranslationViewSet(ModelViewSet):
    queryset = (
        MessageTranslation.objects.select_related(
            "message",
            "target_language_code",
        )
        .all()
        .order_by("id")
    )
    serializer_class = MessageTranslationSerializer
