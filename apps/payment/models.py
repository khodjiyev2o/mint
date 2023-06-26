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
        if self.provider == Provider.FLOW:
            params = {}
            params["apiKey"] = settings.FLOW_API_KEY
            params["commerceOrder"] = self.id
            params["subject"] = self.content.slug
            params["amount"] = self.total_amount
            params["email"] = self.user.email
            params["urlConfirmation"] = settings.BACKEND_URL + reverse("confirm-transaction", kwargs={"pk": self.id})
            params["urlReturn"] = settings.FRONTEND_URL + "/payment/Success"
            params["s"] = signature(**params)
            p = requests.post(settings.FLOW_API_URL + "/payment/create", params)

            data = p.json()
            # Check if there is an error code from flow side
            if data.get("code"):
                return data
            if data["flowOrder"]:
                Transaction.objects.get_or_create(
                    order=self,
                    transaction_id=data["flowOrder"],
                    amount=self.total_amount,
                )
                return {"token": data["token"], "url": f"{data['url']}?token={data['token']}"}


class Transaction(BaseModel):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, verbose_name=_("Order"))
    transaction_id = models.CharField(max_length=255, verbose_name=_("Transaction ID"), null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))
    status = models.CharField(max_length=63, verbose_name=_("Status"), choices=TransactionStatus.choices)
    paid_at = models.DateTimeField(verbose_name=_("Paid At"), null=True, blank=True)
    cancel_time = models.DateTimeField(verbose_name=_("Cancel Time"), null=True, blank=True)

    def __str__(self):
        return f"{self.order} - {self.transaction_id}"

    def apply(self):
        self.status = TransactionStatus.PAID
        self.paid_at = timezone.now()
        self.order.is_paid = True
        self.order.save()
        UserContent.objects.get_or_create(user=self.order.user, content=self.order.content, order=self.order)
        UserContentPaymentPlan.objects.create(
            user=self.order.user, content=self.order.content, order=self.order, payment_plan=self.order.payment_type
        )
        self.save()

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
    card_number = models.CharField(max_length=255, verbose_name=_("Card Number"))
    expire_date = models.CharField(max_length=255, verbose_name=_("Expire Date"))
    card_id = models.CharField(max_length=255, verbose_name=_("Card ID"))
    token = models.CharField(max_length=255, verbose_name=_("Token"), null=True)
    confirmed = models.BooleanField(default=False, verbose_name=_("Confirmed"))

    class Meta:
        verbose_name = _("User Card")
        verbose_name_plural = _("User Cards")
        unique_together = ("user", "card_number")
