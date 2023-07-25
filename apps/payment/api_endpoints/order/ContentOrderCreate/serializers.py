from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.payment.api_endpoints.order.serializers import OrderWithCardSerializer
from apps.payment.models import Order, PaymentType, Provider
from apps.preventa.models import UserContent, UserContentPaymentPlan


class ContentOrderCreateSerializer(OrderWithCardSerializer):
    payment_url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "content", "payment_type", "provider", "total_amount", "payment_url")
        extra_kwargs = {"content": {"required": True}}

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if self.already_bought(attrs):
            raise serializers.ValidationError(
                detail={"content": _("You have already bought this content")}, code="already_bought"
            )
        self.check_total_amount(attrs)
        return attrs

    def already_bought(self, attrs):
        user_payment_plan = UserContentPaymentPlan.objects.filter(
            user=self.context["request"].user, content=attrs["content"]
        ).last()
        # User did not buy anything so far
        if user_payment_plan is None:
            return False
        # User bought the four repr content
        if user_payment_plan.payment_plan == PaymentType.FOUR_TIME:
            return (
                UserContent.objects.filter(user=self.context["request"].user, content=attrs["content"]).exists()
                and user_payment_plan.available_reproductions > 0
            )
        # User bought unlimited one
        if user_payment_plan.payment_plan == PaymentType.FOUR_TIME:
            return (
                UserContent.objects.filter(user=self.context["request"].user, content=attrs["content"]).exists()
                and user_payment_plan.expiration_date >= timezone.now()
            )

    def check_total_amount(self, attrs):
        if attrs["payment_type"] == PaymentType.ONE_MONTH:
            total_amount = attrs["content"].one_month_price

        elif attrs["payment_type"] == PaymentType.FOUR_TIME:
            total_amount = attrs["content"].four_repr_price
        else:
            raise serializers.ValidationError(detail={"payment_type": _("Invalid payment type")}, code="invalid")

        if total_amount != attrs["total_amount"]:
            raise serializers.ValidationError(detail={"total_amount": _("Invalid total amount")}, code="invalid")

    def get_payment_url(self, obj):
        if obj.provider == Provider.FLOW:
            response = obj.get_payment_url()
            if list(response.keys()) == ["code", "message"]:
                raise serializers.ValidationError(detail={"Payment": _(f"{response['message']}")}, code="invalid")
            return response
        return
