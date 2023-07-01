import requests
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView

from apps.payment.models import FlowCustomer, UserCard
from utils.services.encrypt import signature


class CreditCardAddResponseView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        params = {
            "apiKey": settings.FLOW_API_KEY,
            "token": token,
        }
        params["s"] = signature(**params)
        response = requests.get(settings.FLOW_API_URL + "/customer/getRegisterStatus", params).json()
        if response["status"] == "1":
            customer = FlowCustomer.objects.get(flow_customer_id=response["customerId"])
            UserCard.objects.get_or_create(
                user=customer.cliente,
                type=response["creditCardType"],
                last_four_digits=response["last4CardDigits"],
                registration_token=token,
                confirmed=True,
            )

            return redirect(f"{settings.FRONTEND_URL}/payment/Success")
        else:
            return redirect(f"{settings.FRONTEND_URL}/payment/unsuccessfull")


__all__ = ["CreditCardAddResponseView"]
