from rest_framework import serializers

from .models import (
    ChatRoom,
    ChatRoomMember,
    Language,
    Message,
    MessageTranslation,
    User,
)


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    preferred_language_name = serializers.CharField(
        source="preferred_language_code.native_name",
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "nickname",
            "preferred_language_code",
            "preferred_language_name",
            "profile_image_url",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }


class ChatRoomSerializer(serializers.ModelSerializer):
    created_by_nickname = serializers.CharField(source="created_by.nickname", read_only=True)

    class Meta:
        model = ChatRoom
        fields = "__all__"


class ChatRoomMemberSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)
    room_title = serializers.CharField(source="chat_room.title", read_only=True)
    display_language_name = serializers.CharField(
        source="display_language_code.native_name",
        read_only=True,
    )

    class Meta:
        model = ChatRoomMember
        fields = "__all__"

    def validate(self, attrs):
        chat_room = attrs.get("chat_room") or getattr(self.instance, "chat_room", None)
        last_read_message = attrs.get("last_read_message")
        if last_read_message and chat_room and last_read_message.chat_room_id != chat_room.id:
            raise serializers.ValidationError(
                {"last_read_message": "last_read_message must belong to the same chat_room."}
            )
        return attrs


class MessageSerializer(serializers.ModelSerializer):
    sender_nickname = serializers.CharField(source="sender.nickname", read_only=True)
    original_language_name = serializers.CharField(
        source="original_language_code.native_name",
        read_only=True,
    )

    class Meta:
        model = Message
        fields = "__all__"

    def validate(self, attrs):
        chat_room = attrs.get("chat_room") or getattr(self.instance, "chat_room", None)
        sender = attrs.get("sender") or getattr(self.instance, "sender", None)
        if chat_room and sender:
            is_member = ChatRoomMember.objects.filter(chat_room=chat_room, user=sender).exists()
            if not is_member:
                raise serializers.ValidationError(
                    {"sender": "sender must be a member of the chat_room."}
                )
        return attrs


class MessageTranslationSerializer(serializers.ModelSerializer):
    original_content = serializers.CharField(source="message.original_content", read_only=True)
    target_language_name = serializers.CharField(
        source="target_language_code.native_name",
        read_only=True,
    )

    class Meta:
        model = MessageTranslation
        fields = "__all__"

    def validate(self, attrs):
        message = attrs.get("message") or getattr(self.instance, "message", None)
        target_language_code = attrs.get("target_language_code")
        if message and target_language_code and message.original_language_code_id == target_language_code.code:
            raise serializers.ValidationError(
                {"target_language_code": "target_language_code must differ from original_language_code."}
            )
        return attrs
