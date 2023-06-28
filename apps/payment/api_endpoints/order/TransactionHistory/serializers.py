from rest_framework import serializers

from apps.common.models import Content
from apps.payment.models import Order, Transaction


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("uuid", "title", "creator")


class OrderSerializer(serializers.ModelSerializer):
    content = ContentSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "content",
        )


class TransactionHistorySerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Transaction
        fields = ("id", "order", "paid_at", "amount")
