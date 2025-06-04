from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class Region(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Viloyat"))
    soato_id = models.CharField(
        max_length=255,
        verbose_name=_("Soato ID"),
        help_text=_("Soato ID for the region"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Viloyat")
        verbose_name_plural = _("Viloyatlar")
        ordering = ["name"]


class District(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Tuman"))
    region = models.ForeignKey(
        "Region",
        on_delete=models.CASCADE,
        related_name="districts",
        verbose_name=_("Viloyat"),
    )
    soato_id = models.CharField(
        max_length=255,
        verbose_name=_("Soato ID"),
        help_text=_("Soato ID for the district"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tuman")
        verbose_name_plural = _("Tumanlar")
        ordering = ["name"]
