from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentType(models.TextChoices):
    ONE_TIME = "one_time", _("ONE TIME")
    FOUR_TIME_REPRODUCTION = "four_time_reproduction", _("Four Time Reproduction")
    ONE_MONTH = "one_month", _("ONE MONTH")
    ONE_DAY = "one_day", _("ONE DAY")
