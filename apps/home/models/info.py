from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class PedagogInfo(AbstractBaseModel):
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("Title of the pedagog info"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Description of the pedagog info"),
    )
    image = models.ImageField(
        upload_to="pedagog/info/",
        verbose_name=_("Image"),
        help_text=_("Image of the pedagog info"),
    )
    icon = models.CharField(
        max_length=255,
        verbose_name=_("Icon"),
        help_text=_("Icon of the pedagog info"),
    )

    class Meta:
        verbose_name = _("Pedagog Info")
        verbose_name_plural = _("Pedagog Info")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
