from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel
from apps.users.models.user import User


class ResetToken(AbstractBaseModel):
    token = models.CharField(max_length=255, unique=True, verbose_name=_("Token"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi")
    )

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = _("Tokenni tiklash")
        verbose_name_plural = _("Tokenni tiklash")
