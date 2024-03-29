import sys

import requests
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.enums import PaymentType, Provider, TransactionStatus
from apps.common.models import BaseModel
from apps.preventa.models import UserContent, UserContentPaymentPlan
from utils.services.encrypt import signature


class Order(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("User"))
    content = models.ForeignKey(
        "common.content",
        on_delete=models.CASCADE,
        verbose_name=_("Content"),
        null=True,
        blank=True,
        related_name="orders",
    )
    user_card = models.ForeignKey(
        "UserCard", on_delete=models.PROTECT, verbose_name=_("User card"), null=True, blank=True, related_name="orders"
    )
    payment_type = models.CharField(max_length=63, verbose_name=_("Payment Type"), choices=PaymentType.choices)
    provider = models.CharField(max_length=63, verbose_name=_("Provider"), choices=Provider.choices)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"))
    is_paid = models.BooleanField(default=False, verbose_name=_("Is Paid"))
    is_canceled = models.BooleanField(default=False, verbose_name=_("Is Canceled"))

    def __str__(self):
        return f"{self.user} - {self.content}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def get_payment_url(self):
        if "test" not in sys.argv:
            params = {
                "apiKey": settings.FLOW_API_KEY,
                "commerceOrder": self.id,
                "subject": self.content.slug,
                "amount": self.total_amount,
                "email": self.user.email,
                "urlConfirmation": settings.BACKEND_URL + reverse("confirm-transaction", kwargs={"pk": self.id}),
                "urlReturn": settings.FRONTEND_URL + "/payment/Success",
            }
            if self.provider == Provider.FLOW:
                params["s"] = signature(**params)
                response = requests.post(settings.FLOW_API_URL + "/payment/create", params).json()

                # Check if there is an error code from flow side
                if response.get("code"):
                    return response
                if response["flowOrder"]:
                    Transaction.objects.get_or_create(
                        order=self,
                        transaction_id=response["flowOrder"],
                        amount=self.total_amount,
                    )
                    return {"token": response["token"], "url": f"{response['url']}?token={response['token']}"}
            elif self.provider == Provider.CARD:
                return "Payment with Card"
        return {"url": "test"}


class Transaction(BaseModel):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, verbose_name=_("Order"))
    transaction_id = models.CharField(max_length=255, verbose_name=_("Transaction ID"), null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))
    status = models.CharField(
        max_length=63, verbose_name=_("Status"), choices=TransactionStatus.choices, default=TransactionStatus.WAITING
    )
    paid_at = models.DateTimeField(verbose_name=_("Paid At"), null=True, blank=True)
    cancel_time = models.DateTimeField(verbose_name=_("Cancel Time"), null=True, blank=True)

    def __str__(self):
        return f"{self.order} - {self.transaction_id}"

    def apply(self):
        self.status = TransactionStatus.PAID
        self.paid_at = timezone.now()
        self.save()

        self.order.is_paid = True
        self.order.save()

        UserContent.objects.get_or_create(user=self.order.user, content=self.order.content, order=self.order)
        UserContentPaymentPlan.objects.create(
            user=self.order.user,
            content=self.order.content,
            order=self.order,
            payment_plan=self.order.payment_type,
        )

    def cancel(self):
        self.status = TransactionStatus.CANCELED
        self.cancel_time = timezone.now()
        UserContent.objects.get_or_create(user=self.order.user, content=self.order.content, order=self.order).delete()

        self.save()
        self.order.is_paid = False
        self.order.is_canceled = True
        self.order.save()

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")


class UserCard(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("User"))
    type = models.CharField(max_length=255, verbose_name=_("Type"))
    last_four_digits = models.CharField(max_length=255, verbose_name=_("Last Four Digits"))
    registration_token = models.CharField(max_length=255, verbose_name=_("Registration Token"), null=True)
    confirmed = models.BooleanField(default=False, verbose_name=_("Confirmed"))

    def __str__(self):
        return f"{self.user} | {self.type}"

    class Meta:
        verbose_name = _("User Card")
        verbose_name_plural = _("User Cards")


class FlowCustomer(BaseModel):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    cliente = models.ForeignKey("users.User", on_delete=models.PROTECT, related_name="flow_customer")
    flow_customer_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cliente.email}"

    class Meta:
        verbose_name = _("Flow Customer")
        verbose_name_plural = _("Flow Customers")
        unique_together = ("cliente", "flow_customer_id")

    def set_and_get_customer_id(self, user):
        params = {
            "apiKey": settings.FLOW_API_KEY,
            "name": self.name,
            "email": self.cliente.email,
            "externalId": self.cliente.email,
        }
        params["s"] = signature(**params)
        p = requests.post(settings.FLOW_API_URL + "/customer/create", params)
        data = p.json()

        status = data.get("status", None)
        flow_customer_id = data.get("customerId", None)
        code = data.get("code", None)

        # if status is okay and customer is new , save it
        if status == 1 and flow_customer_id is not None:
            self.flow_customer_id = flow_customer_id
            self.save()
            return flow_customer_id

        # if customer is already registered , return from our db
        elif code == 501:
            try:
                return FlowCustomer.objects.get(cliente=user).flow_customer_id
            except FlowCustomer.DoesNotExist:
                return None
        return None
