from rest_framework.serializers import ModelSerializer
from .models import Notice, Source, SourceSubscription, InboxNotice
from accounts.serializers import UserIdUsernameSerializer


class NoticeSerializer(ModelSerializer):
  class Meta:
    model = Notice
    fields = "__all__"

class SourceSerializer(ModelSerializer):
  class Meta:
    model = Source
    fields = "__all__"

class SourceSubscriptionSerializer(ModelSerializer):
  user = UserIdUsernameSerializer(read_only=True)
  source = SourceSerializer(read_only=True)
  class Meta:
    model = SourceSubscription
    fields = "__all__"

class InboxNoticeSerializer(ModelSerializer):
  user = UserIdUsernameSerializer(read_only=True)
  notice = NoticeSerializer(read_only=True)
  class Meta:
    model = InboxNotice
    fields = "__all__"
