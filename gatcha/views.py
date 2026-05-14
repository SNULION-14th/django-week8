import random

from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import (
    GatchaItemList,
    GatchaPoolItem,
    GatchaType,
    User,
    UserGatchaRecord,
    UserItemList,
)
from .request_serializers import ChargeCurrencyRequestSerializer, DrawGatchaRequestSerializer
from .serializers import (
    GatchaItemListSerializer,
    GatchaPoolItemSerializer,
    GatchaTypeSerializer,
    UserGatchaRecordSerializer,
    UserItemListSerializer,
    UserSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by("user_id")
    serializer_class = UserSerializer
    lookup_field = "user_id"
    lookup_url_kwarg = "user_id"

    @extend_schema(
        summary="Charge currency",
        description="Increase a user's currency balance.",
        request=ChargeCurrencyRequestSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Bad Request"),
            404: OpenApiResponse(description="Not Found"),
        },
    )
    @action(detail=True, methods=["post"])
    def charge(self, request, user_id=None):
        request_serializer = ChargeCurrencyRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.currency_balance += request_serializer.validated_data["amount"]
        user.save(update_fields=["currency_balance"])

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="User inventory",
        description="Return all items owned by one user.",
        responses={200: UserItemListSerializer(many=True)},
    )
    @action(detail=True, methods=["get"])
    def inventory(self, request, user_id=None):
        user = self.get_object()
        inventory_items = UserItemList.objects.select_related("user", "item").filter(user=user)
        serializer = UserItemListSerializer(inventory_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="User gatcha records",
        description="Return draw records for one user.",
        responses={200: UserGatchaRecordSerializer(many=True)},
    )
    @action(detail=True, methods=["get"])
    def records(self, request, user_id=None):
        user = self.get_object()
        records = UserGatchaRecord.objects.select_related("user", "gatcha", "item").filter(user=user)
        serializer = UserGatchaRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GatchaTypeViewSet(ModelViewSet):
    queryset = GatchaType.objects.all().order_by("gatcha_id")
    serializer_class = GatchaTypeSerializer
    lookup_field = "gatcha_id"
    lookup_url_kwarg = "gatcha_id"


class GatchaItemViewSet(ModelViewSet):
    queryset = GatchaItemList.objects.all().order_by("item_id")
    serializer_class = GatchaItemListSerializer
    lookup_field = "item_id"
    lookup_url_kwarg = "item_id"


class GatchaPoolItemViewSet(ModelViewSet):
    queryset = GatchaPoolItem.objects.select_related("gatcha", "item").order_by("pool_item_id")
    serializer_class = GatchaPoolItemSerializer
    lookup_field = "pool_item_id"
    lookup_url_kwarg = "pool_item_id"


class GatchaDrawViewSet(ViewSet):
    @extend_schema(
        summary="Draw gatcha",
        description="Spend user currency, draw one item from the gatcha pool, and save the result.",
        request=DrawGatchaRequestSerializer,
        responses={
            201: UserGatchaRecordSerializer,
            400: OpenApiResponse(description="Bad Request"),
            404: OpenApiResponse(description="Not Found"),
        },
    )
    @transaction.atomic
    def create(self, request):
        request_serializer = DrawGatchaRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        data = request_serializer.validated_data

        user = get_object_or_404(
            User.objects.select_for_update(),
            user_id=data["user_id"],
        )
        gatcha = get_object_or_404(GatchaType, gatcha_id=data["gatcha_id"])

        now = timezone.now()
        if not (gatcha.start_date <= now <= gatcha.end_date):
            return Response({"detail": "Gatcha is not active."}, status=status.HTTP_400_BAD_REQUEST)

        if user.currency_balance < gatcha.price:
            return Response({"detail": "Not enough currency."}, status=status.HTTP_400_BAD_REQUEST)

        pool_items = list(GatchaPoolItem.objects.select_related("item").filter(gatcha=gatcha))
        if not pool_items:
            return Response({"detail": "Gatcha pool is empty."}, status=status.HTTP_400_BAD_REQUEST)

        selected_pool_item = self._pick_pool_item(pool_items)

        user.currency_balance -= gatcha.price
        user.save(update_fields=["currency_balance"])

        inventory, created = UserItemList.objects.get_or_create(
            user=user,
            item=selected_pool_item.item,
            defaults={"quantity": 0},
        )
        inventory.quantity += 1
        inventory.save(update_fields=["quantity"])

        record = UserGatchaRecord.objects.create(
            user=user,
            gatcha=gatcha,
            item=selected_pool_item.item,
        )

        serializer = UserGatchaRecordSerializer(record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _pick_pool_item(self, pool_items):
        total_rate = sum(float(pool_item.drop_rate) for pool_item in pool_items)
        if total_rate <= 0:
            return random.choice(pool_items)

        target = random.uniform(0, total_rate)
        cumulative_rate = 0
        for pool_item in pool_items:
            cumulative_rate += float(pool_item.drop_rate)
            if target <= cumulative_rate:
                return pool_item

        return pool_items[-1]
