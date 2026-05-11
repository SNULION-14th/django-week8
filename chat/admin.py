from django.contrib import admin

from .models import (
    ChatRoom,
    ChatRoomMember,
    Language,
    Message,
    MessageTranslation,
    User,
)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "native_name")
    search_fields = ("code", "name", "native_name")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "nickname", "preferred_language_code", "created_at")
    list_filter = ("preferred_language_code",)
    search_fields = ("email", "nickname")


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_type", "title", "created_by", "created_at")
    list_filter = ("room_type",)
    search_fields = ("title", "created_by__nickname")


@admin.register(ChatRoomMember)
class ChatRoomMemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "chat_room",
        "user",
        "display_language_code",
        "joined_at",
        "left_at",
        "last_read_message",
    )
    list_filter = ("display_language_code", "joined_at")
    search_fields = ("user__email", "user__nickname", "chat_room__title")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "chat_room",
        "sender",
        "original_language_code",
        "message_type",
        "created_at",
    )
    list_filter = ("message_type", "original_language_code", "created_at")
    search_fields = ("original_content", "sender__nickname")


@admin.register(MessageTranslation)
class MessageTranslationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "message",
        "target_language_code",
        "translation_status",
        "provider",
        "created_at",
    )
    list_filter = ("target_language_code", "translation_status", "provider")
    search_fields = ("translated_content",)
