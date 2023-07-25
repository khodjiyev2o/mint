import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


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
    one_month_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    four_repr_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def clean(self):
        """Check if creator profile is enabled"""

        if self.creator.is_creator is False:
            raise ValidationError(_("User should be creator to publish content"))

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Content, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


__all__ = ["Content", "BaseModel"]
