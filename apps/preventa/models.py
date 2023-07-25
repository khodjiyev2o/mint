import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.common.enums import PaymentType
from apps.common.models import BaseModel, Content
from config.storage_backends import PrivateMediaStorage
from utils.services.slugify import unique_slugify


class Audio(Content):
    cover = models.FileField(null=True, blank=True, upload_to="preventa/audio/cover/%Y/%m")
    file = models.FileField(null=True, blank=True, upload_to="preventa/audio/file/%Y/%m", storage=PrivateMediaStorage())
    duration_seconds = models.PositiveIntegerField(default=0, verbose_name=_("Duration in seconds"))

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it doesn't exist
            self.slug = unique_slugify(self, slugify(self.title))

        super().save(*args, **kwargs)

    def is_bought(self, user):
        user_payment_plan = UserContentPaymentPlan.objects.filter(user=user, content=self).last()
        if user_payment_plan is None:
            return False
        if user_payment_plan.payment_plan == PaymentType.FOUR_TIME:
            return (
                UserContent.objects.filter(user=user, content=self).exists()
                and user_payment_plan.available_reproductions > 0
            )
        if user_payment_plan.payment_plan == PaymentType.ONE_MONTH:
            return user_payment_plan.expiration_date >= timezone.now()


class UserContent(BaseModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_content", verbose_name=_("User")
    )
    content = models.ForeignKey(Content, verbose_name=_("Content"), on_delete=models.CASCADE)
    order = models.OneToOneField("payment.Order", on_delete=models.CASCADE, verbose_name=_("Order"))

    def __str__(self):
        return str(self.content.title)

    def clean(self):
        """Check if payment is  successfull"""

        if self.order.is_paid is False:
            raise ValidationError(_("The payment is not successfull yet"))

    def save(self, *args, **kwargs):
        self.full_clean()
        super(UserContent, self).save(*args, **kwargs)


class UserContentPaymentPlan(BaseModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_content_payment_plans", verbose_name=_("User")
    )
    order = models.OneToOneField("payment.Order", on_delete=models.CASCADE, verbose_name=_("Order"))
    content = models.ForeignKey(
        Content, verbose_name=_("Content"), on_delete=models.CASCADE, related_name="user_content_plan"
    )
    payment_plan = models.CharField(
        _("Type"), max_length=255, choices=PaymentType.choices, default=PaymentType.ONE_TIME
    )
    available_reproductions = models.IntegerField(default=4, help_text="Used when content is bought for 4 repro...")
    expiration_date = models.DateTimeField(null=True, blank=True)

    def clean(self):
        """Check if payment is  successfull"""

        if self.order.is_paid is False:
            raise ValidationError(_("The payment is not successfull yet"))

    def save(self, *args, **kwargs):
        self.full_clean()

        # Check if the instance is being created for the first time
        if not self.pk and self.payment_plan == PaymentType.ONE_MONTH:
            # Calculate the new expiration date as current date + 30 days
            self.expiration_date = datetime.datetime.now() + datetime.timedelta(days=30)

        super(UserContentPaymentPlan, self).save(*args, **kwargs)
