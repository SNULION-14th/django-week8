from rest_framework import serializers
from accounts.request_serializers import SignInRequestSerializer

class SourceSubscriptionListRequestSerializer(serializers.Serializer):
  user = SignInRequestSerializer()
  source_name = serializers.CharField()
  source_url = serializers.URLField()
  source_crawl_interval_minutes = serializers.IntegerField()

class SourceSubscriptionDetailRequestSerializer(serializers.Serializer):
  user = SignInRequestSerializer()
  source_name = serializers.CharField()
  source_url = serializers.URLField()
  source_crawl_interval_minutes = serializers.IntegerField()
