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


class UserContent(BaseModel):
    preventa_audio = models.ForeignKey(
        Audio,
        verbose_name=_("Bought Audio"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    order = models.OneToOneField("payment.Order", on_delete=models.CASCADE, verbose_name=_("Order"))
    watched_time = models.PositiveIntegerField(default=4, help_text="Used when content is bought for 4 repro...")

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
