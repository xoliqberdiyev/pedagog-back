from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class ScienceLanguage(AbstractBaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("The name of the science language."),
        db_index=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Indicates whether the science language is currently active."),
    )

    class Meta:
        verbose_name = _("Science Language")
        verbose_name_plural = _("Science Languages")
        ordering = ["name"]

    def __str__(self):
        return f"ID: {self.id} - {self.name}"


class Science(AbstractBaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("The name of the science subject."),
        db_index=True,
    )
    language = models.ManyToManyField(
        "ScienceLanguage",
        verbose_name=_("Languages"),
        help_text=_("The languages in which this science subject is taught."),
        related_name="sciences",
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Indicates whether the science is currently active."),
    )

    class Meta:
        verbose_name = _("Science")
        verbose_name_plural = _("Sciences")
        ordering = ["name"]

    def __str__(self):
        return f"{self.id} - {self.name}"
