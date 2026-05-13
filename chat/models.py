from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    native_name = models.CharField(max_length=50)

    class Meta:
        db_table = "chat_languages"

    def __str__(self):
        return f"{self.native_name} ({self.code})"


class User(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=50)
    preferred_language_code = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        db_column="preferred_language_code",
        related_name="preferred_users",
    )
    profile_image_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "chat_users"
        verbose_name = "chat user"
        verbose_name_plural = "chat users"

    def __str__(self):
        return self.nickname


class ChatRoom(models.Model):
    class RoomType(models.TextChoices):
        DIRECT = "DM", "Direct message"
        GROUP = "GROUP", "Group chat"

    room_type = models.CharField(
        max_length=20,
        choices=RoomType.choices,
        default=RoomType.DIRECT,
    )
    title = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_column="created_by",
        related_name="created_chat_rooms",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "chat_rooms"

    def __str__(self):
        return self.title or f"{self.room_type} room #{self.pk}"


class Message(models.Model):
    class MessageType(models.TextChoices):
        TEXT = "TEXT", "Text"
        IMAGE = "IMAGE", "Image"
        FILE = "FILE", "File"

    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        db_column="chat_room_id",
        related_name="messages",
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="sender_id",
        related_name="sent_messages",
    )
    original_language_code = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        db_column="original_language_code",
        related_name="original_messages",
    )
    original_content = models.TextField()
    message_type = models.CharField(
        max_length=20,
        choices=MessageType.choices,
        default=MessageType.TEXT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "chat_messages"

    def __str__(self):
        return self.original_content[:30]


class ChatRoomMember(models.Model):
    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        db_column="chat_room_id",
        related_name="members",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="chat_room_memberships",
    )
    display_language_code = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        db_column="display_language_code",
        related_name="chat_room_members",
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    last_read_message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        db_column="last_read_message_id",
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        db_table = "chat_room_members"
        constraints = [
            models.UniqueConstraint(
                fields=["chat_room", "user"],
                name="unique_chat_room_member",
            ),
        ]

    def __str__(self):
        return f"{self.user} in {self.chat_room}"


class MessageTranslation(models.Model):
    class TranslationStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        DONE = "DONE", "Done"
        FAILED = "FAILED", "Failed"

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        db_column="message_id",
        related_name="translations",
    )
    target_language_code = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        db_column="target_language_code",
        related_name="message_translations",
    )
    translated_content = models.TextField()
    translation_status = models.CharField(
        max_length=20,
        choices=TranslationStatus.choices,
        default=TranslationStatus.PENDING,
    )
    provider = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "chat_message_translations"
        constraints = [
            models.UniqueConstraint(
                fields=["message", "target_language_code"],
                name="unique_message_translation_language",
            ),
        ]

    def __str__(self):
        return f"{self.message_id} -> {self.target_language_code_id}"
