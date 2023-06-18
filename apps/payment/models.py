from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


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
    audio = models.ForeignKey(
        "preventa.audio",
        on_delete=models.CASCADE,
        verbose_name=_("Audio"),
        null=True,
        blank=True,
        related_name="orders",
    )
    user_card = models.ForeignKey(
        "UserCard", on_delete=models.PROTECT, verbose_name=_("User card"), null=True, blank=True, related_name="orders"
    )
    type = models.CharField(max_length=63, verbose_name=_("Type"), choices=OrderType.choices)
    payment_type = models.CharField(max_length=63, verbose_name=_("Payment Type"), choices=PaymentType.choices)
    provider = models.CharField(max_length=63, verbose_name=_("Provider"), choices=Provider.choices)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"))
    is_paid = models.BooleanField(default=False, verbose_name=_("Is Paid"))
    is_canceled = models.BooleanField(default=False, verbose_name=_("Is Canceled"))

    def __str__(self):
        if self.type == OrderType.AUDIO:
            return f"{self.user} - {self.audio}"
        return f"{self.user}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


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
