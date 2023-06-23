import requests
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from utils.services.encrypt import signature


class OrderType(models.TextChoices):
    AUDIO = "audio", _("Audio")


class PaymentType(models.TextChoices):
    ONE_TIME = "one_time", _("One Time")
    FOUR_TIME = "four_time", _("Four Time")
    ONE_MONTH = "one_month", _("One Month")
    ONE_DAY = "one_day", _("One Day")


class Provider(models.TextChoices):
    FLOW = "flow", _("FLOW")


class TransactionStatus(models.TextChoices):
    WAITING = "waiting", _("Waiting")
    PAID = "paid", _("Paid")
    FAILED = "failed", _("Failed")
    CANCELED = "canceled", _("Canceled")


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
            params["urlConfirmation"] = settings.FRONTEND_URL + "/payment/Success"
            params["urlReturn"] = settings.FRONTEND_URL + "/payment/Success"
            params["s"] = signature(**params)
            p = requests.post(settings.FLOW_API_URL + "/payment/create", params)
            data = p.json()
            return {"token": data["token"], "url": f"{data['url']}?token={data['token']}"}


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
