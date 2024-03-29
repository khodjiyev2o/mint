from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.models import BaseModel

from .managers import UserManager


class User(AbstractUser, BaseModel):
    first_name = models.CharField(_("First Name"), max_length=255, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=255, null=True, blank=True)
    username = models.CharField(_("Username"), max_length=255, unique=True, null=True, blank=True)
    email = models.EmailField(_("Email"), max_length=255, unique=True)
    photo = models.ImageField(_("Photo"), upload_to="users/%Y/%m", blank=True, null=True)
    is_creator = models.BooleanField(_("Is Creator"), default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # type: ignore

    def __str__(self):
        if self.first_name:
            return self.first_name

        return self.email

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.last_name:
            return f"{self.last_name}"
        if self.first_name:
            return f"{self.first_name}"

    @property
    def tokens(self):
        token = RefreshToken.for_user(self)
        return {"access": str(token.access_token), "refresh": str(token)}

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


__all__ = ["User"]
