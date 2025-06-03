from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class ContactUs(AbstractBaseModel):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    phone = models.CharField(_("phone"), max_length=20)
    text = models.TextField(_("text"))

    class Meta:
        verbose_name = _("contact us")
        verbose_name_plural = _("contact us")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
