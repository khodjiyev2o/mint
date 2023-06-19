import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.enums import PaymentType


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class Content(BaseModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    title = models.CharField(verbose_name=_("Title"), max_length=256)
    creator = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def clean(self):
        """Check if creator profile is enabled"""

        if self.creator.is_creator is False:
            raise ValidationError(_("User should be creator to publish content"))

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Content, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class PaymentPlan(BaseModel):
    content = models.ForeignKey(
        Content, verbose_name=_("Content"), on_delete=models.CASCADE, related_name="payment_plans"
    )
    type = models.CharField(_("Type"), max_length=255, choices=PaymentType.choices, default=PaymentType.ONE_TIME)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_("Price"))

    def __str__(self):
        return f"{self.type}"


__all__ = ["PaymentPlan", "Content", "BaseModel"]
