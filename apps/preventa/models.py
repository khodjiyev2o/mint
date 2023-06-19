from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel, Content
from utils.services.slugify import unique_slugify


class Audio(Content):
    cover = models.FileField(null=True, blank=True, upload_to="preventa/audio/cover/%Y/%m")
    file = models.FileField(null=True, blank=True, upload_to="preventa/audio/file/%Y/%m")
    duration_seconds = models.PositiveIntegerField(default=0, verbose_name=_("Duration in seconds"))

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it doesn't exist
            self.slug = unique_slugify(self, slugify(self.title))

        super().save(*args, **kwargs)

    def is_bought(self, user):
        return (
            UserContent.objects.filter(user=user, preventa_audio=self).exists()
            and UserContentPaymentPlan.objects.filter(user=user, content=self).first().available_reproductions > 0
        )


class UserContent(BaseModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_preventa_audios", verbose_name=_("User")
    )
    preventa_audio = models.ForeignKey(
        Audio,
        verbose_name=_("Bought Audio"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    order = models.OneToOneField("payment.Order", on_delete=models.CASCADE, verbose_name=_("Order"))

    def __str__(self):
        if self.preventa_audio:
            return str(self.preventa_audio.title)

    def clean(self):
        """Check if payment is  successfull"""

        if self.order.is_paid is False:
            raise ValidationError(_("The payment is successfull yet"))

    def save(self, *args, **kwargs):
        self.full_clean()
        super(UserContent, self).save(*args, **kwargs)


class UserContentPaymentPlan(BaseModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_content_payment_plans", verbose_name=_("User")
    )
    content = models.ForeignKey(
        Content, verbose_name=_("Content"), on_delete=models.CASCADE, related_name="user_payment_plans"
    )
    payment_plan = models.ForeignKey("common.PaymentPlan", verbose_name=_("Payment Plan"), on_delete=models.CASCADE)
    available_reproductions = models.IntegerField(default=4, help_text="Used when content is bought for 4 repro...")
