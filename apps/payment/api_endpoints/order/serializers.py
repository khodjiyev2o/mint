import requests
from django.conf import settings
from django.db import transaction as db_transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.payment.models import FlowCustomer, Provider, Transaction, TransactionStatus
from utils.services.encrypt import signature


class OrderWithCardSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs["provider"] == Provider.CARD:
            flow_customer = FlowCustomer.objects.filter(cliente=self.context["request"].user)

            if not flow_customer.exists():
                raise serializers.ValidationError(
                    detail={"user": _("User has not been registered in Flow")}, code="not registered"
                )

        return attrs

    def create(self, validated_data):
        if validated_data["provider"] != Provider.CARD:
            return super().create(validated_data)

        with db_transaction.atomic():
            order = super().create(validated_data)
            error, response, transaction = self.pay_with_card(order)

        if error:
            if transaction:
                transaction.status = TransactionStatus.FAILED
                transaction.save()

            if response["code"] == 1605:
                raise serializers.ValidationError(
                    detail={"order": _("This commerceOrder  has been previously paid")},
                    code="order_already_paid",
                )
            else:
                raise serializers.ValidationError(
                    detail={"user_card": _("Something went wrong")}, code="something_went_wrong"
                )

        transaction.apply()
        return order

    @staticmethod
    def pay_with_card(order) -> tuple:
        customer_id = FlowCustomer.objects.filter(cliente=order.user)[0].flow_customer_id
        params = {
            "apiKey": settings.FLOW_API_KEY,
            "commerceOrder": order.id,
            "amount": order.total_amount,
            "subject": order.content.slug,
            "customerId": customer_id,
        }
        params["s"] = signature(**params)
        response = requests.post(settings.FLOW_API_URL + "/customer/charge", params).json()
        # if order is already paid
        if response.get("code", None) is not None and response.get("message", None) is not None:
            return True, response, None

        transaction = Transaction.objects.create(
            order=order,
            transaction_id=response["flowOrder"],
            amount=order.total_amount,
            status=TransactionStatus.WAITING,
        )
        # success
        if response["status"] == 2:
            return False, response, transaction
        # pending
        elif response["status"] == 1:
            return True, response, None
        # failure
        else:
            return True, response, transaction
