from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.pedagog.models.classes import Classes
from apps.shared.models.base import AbstractBaseModel


class SchoolType(AbstractBaseModel):
    """
    Model representing the type of a school.
    """

    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("The name of the school type."),
        db_index=True,
    )
    classes = models.ManyToManyField(
        Classes,
        verbose_name=_("Classes"),
        help_text=_("The classes that belong to this school type."),
        related_name="school_types",
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Indicates whether the school type is currently active."),
    )

    class Meta:
        verbose_name = _("School Type")
        verbose_name_plural = _("School Types")
        ordering = ["name"]

    def __str__(self):
        return self.name
