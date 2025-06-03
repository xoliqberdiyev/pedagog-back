from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class Degree(AbstractBaseModel):
    """
    Model representing a degree or qualification.
    """

    name = models.CharField(max_length=255, unique=True, verbose_name=_("Degree Name"))

    class Meta:
        verbose_name = _("Degree")
        verbose_name_plural = _("Degrees")
        ordering = ["name"]

    def __str__(self):
        return self.name
