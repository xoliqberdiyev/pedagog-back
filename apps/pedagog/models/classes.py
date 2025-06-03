from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class Classes(AbstractBaseModel):
    """
    Model representing a class in a school.
    """

    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("The name of the class."),
        db_index=True,
    )
    science = models.ManyToManyField(
        "Science",
        verbose_name=_("Sciences"),
        help_text=_("The science subjects taught in this class."),
        related_name="classes",
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Indicates whether the class is currently active."),
    )

    class Meta:
        verbose_name = _("Class")
        verbose_name_plural = _("Classes")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class ClassGroup(AbstractBaseModel):
    """
    Model representing a group of classes.
    """

    name = models.CharField(
        max_length=20,
        verbose_name=_("Name"),
        help_text=_("The name of the class group."),
        db_index=True,
    )

    class Meta:
        verbose_name = _("Class Group")
        verbose_name_plural = _("Class Groups")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
