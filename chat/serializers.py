from rest_framework.serializers import ModelSerializer

from .models import (
    ChatRoom,
    ChatRoomMember,
    Language,
    Message,
    MessageTranslation,
    User,
)


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
        }


class ChatRoomSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = "__all__"


class ChatRoomMemberSerializer(ModelSerializer):
    class Meta:
        model = ChatRoomMember
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MessageTranslationSerializer(ModelSerializer):
    class Meta:
        model = MessageTranslation
        fields = "__all__"
