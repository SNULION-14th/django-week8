from rest_framework import serializers


class UserRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    nickname = serializers.CharField(max_length=50)
    currency_balance = serializers.IntegerField(min_value=0, required=False, default=0)


class GatchaTypeRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    price = serializers.IntegerField(min_value=0)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()


class GatchaItemRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    grade = serializers.CharField(max_length=10)
    description = serializers.CharField()


class GatchaPoolItemRequestSerializer(serializers.Serializer):
    gatcha_id = serializers.IntegerField(min_value=1)
    item_id = serializers.IntegerField(min_value=1)
    drop_rate = serializers.DecimalField(max_digits=5, decimal_places=4, min_value=0)


class DrawGatchaRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
    gatcha_id = serializers.IntegerField(min_value=1)


class ChargeCurrencyRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
