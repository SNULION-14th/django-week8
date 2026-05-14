from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import (
    GatchaItemList,
    GatchaPoolItem,
    GatchaType,
    User,
    UserGatchaRecord,
    UserItemList,
)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "email", "nickname", "currency_balance", "created_at"]
        read_only_fields = ["user_id", "created_at"]
        ref_name = "GatchaUser"


class GatchaTypeSerializer(ModelSerializer):
    class Meta:
        model = GatchaType
        fields = ["gatcha_id", "title", "price", "start_date", "end_date"]
        read_only_fields = ["gatcha_id"]

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("start_date must be earlier than end_date.")
        return attrs


class GatchaItemListSerializer(ModelSerializer):
    class Meta:
        model = GatchaItemList
        fields = ["item_id", "name", "grade", "description"]
        read_only_fields = ["item_id"]


class GatchaPoolItemSerializer(ModelSerializer):
    gatcha = GatchaTypeSerializer(read_only=True)
    item = GatchaItemListSerializer(read_only=True)
    gatcha_id = serializers.PrimaryKeyRelatedField(
        queryset=GatchaType.objects.all(),
        source="gatcha",
        write_only=True,
    )
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=GatchaItemList.objects.all(),
        source="item",
        write_only=True,
    )

    class Meta:
        model = GatchaPoolItem
        fields = ["pool_item_id", "gatcha", "gatcha_id", "item", "item_id", "drop_rate"]
        read_only_fields = ["pool_item_id"]


class UserGatchaRecordSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    gatcha = GatchaTypeSerializer(read_only=True)
    item = GatchaItemListSerializer(read_only=True)

    class Meta:
        model = UserGatchaRecord
        fields = ["record_id", "user", "gatcha", "item", "created_at"]
        read_only_fields = ["record_id", "created_at"]


class UserItemListSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    item = GatchaItemListSerializer(read_only=True)

    class Meta:
        model = UserItemList
        fields = ["inventory_id", "user", "item", "quantity", "acquired_at"]
        read_only_fields = ["inventory_id", "acquired_at"]
