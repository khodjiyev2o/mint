import requests
from django.conf import settings
from django.urls import reverse
from rest_framework import serializers

from apps.payment.models import FlowCustomer
from utils.services.encrypt import signature


class FlowCustomerCreateSerializer(serializers.ModelSerializer):
    credit_card_register_url = serializers.SerializerMethodField()

    class Meta:
        model = FlowCustomer
        fields = ("name", "credit_card_register_url")

    def get_credit_card_register_url(self, obj):
        user = self.context["request"].user

        customer_id = obj.set_and_get_customer_id(user=user)

        return self.addCreditCard(customer_id=customer_id)

    def create(self, validated_data):
        user = self.context["request"].user

        user, _ = FlowCustomer.objects.get_or_create(cliente=user)
        return user

    @staticmethod
    def addCreditCard(customer_id: str) -> str:
        params = {
            "apiKey": settings.FLOW_API_KEY,
            "customerId": customer_id,
            "url_return": settings.BACKEND_URL + reverse("flow_credit_card_response"),
        }
        params["s"] = signature(**params)
        p = requests.post(settings.FLOW_API_URL + "/customer/register", params)
        data = p.json()

        return data["url"] + "?token=" + data["token"]
