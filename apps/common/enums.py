from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentType(models.TextChoices):
    ONE_TIME = "one_time", _("One Time")
    FOUR_TIME = "four_time", _("Four Time")
    ONE_MONTH = "one_month", _("One Month")
    ONE_DAY = "one_day", _("One Day")


class Provider(models.TextChoices):
    FLOW = "flow", _("FLOW")
    CARD = "card", _("CARD")


class TransactionStatus(models.TextChoices):
    WAITING = "waiting", _("Waiting")
    PAID = "paid", _("Paid")
    FAILED = "failed", _("Failed")
    CANCELED = "canceled", _("Canceled")


class OrderType(models.TextChoices):
    AUDIO = "audio", _("Audio")
