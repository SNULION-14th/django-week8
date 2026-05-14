from rest_framework import serializers


class DetailResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
