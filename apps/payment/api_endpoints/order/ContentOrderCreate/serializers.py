from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.payment.models import Order, PaymentType
from apps.preventa.models import UserContent


class ContentOrderCreateSerializer(serializers.ModelSerializer):
    payment_url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "content", "payment_type", "provider", "total_amount", "payment_url")
        extra_kwargs = {"content": {"required": True}}

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if UserContent.objects.filter(content=attrs["content"], user=self.context["request"].user).exists():
            raise serializers.ValidationError(
                detail={"content": _("You have already bought this audio")}, code="already_bought"
            )
        self.check_total_amount(attrs)
        return attrs

    def check_total_amount(self, attrs):
        if attrs["payment_type"] == PaymentType.ONE_TIME:
            total_amount = attrs["content"].price

        elif attrs["payment_type"] == PaymentType.FOUR_TIME:
            total_amount = attrs["content"].four_repr_price
        else:
            raise serializers.ValidationError(detail={"payment_type": _("Invalid payment type")}, code="invalid")

        if total_amount != attrs["total_amount"]:
            raise serializers.ValidationError(detail={"total_amount": _("Invalid total amount")}, code="invalid")

    def get_payment_url(self, obj):
        return obj.get_payment_url()
