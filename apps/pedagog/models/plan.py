from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.pedagog.models.classes import Classes
from apps.pedagog.models.quarter import Quarter
from apps.pedagog.models.school import SchoolType
from apps.pedagog.models.science import Science, ScienceLanguage
from apps.shared.models.base import AbstractBaseModel


class Plan(AbstractBaseModel):
    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))
    hour = models.IntegerField(default=0, null=True, blank=True, verbose_name=_("Soat"))
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="plans"
    )
    quarter = models.ForeignKey(
        Quarter, on_delete=models.CASCADE, verbose_name=_("Chorak")
    )
    school_type = models.ForeignKey(
        SchoolType,
        on_delete=models.CASCADE,
        verbose_name=_("Maktab turi"),
        related_name="plans",
        null=True,
        blank=True,
    )
    classes = models.ForeignKey(
        Classes,
        on_delete=models.CASCADE,
        verbose_name=_("Sinf"),
        related_name="plans",
    )
    science = models.ForeignKey(
        Science,
        on_delete=models.CASCADE,
        verbose_name=_("Fan"),
        related_name="plans",
    )
    science_language = models.ForeignKey(
        ScienceLanguage,
        on_delete=models.CASCADE,
        verbose_name=_("Fan tili"),
        related_name="plans",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"ID: {self.id}"

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        self.hour = self.topics.aggregate(models.Sum("hours"))["hours__sum"] or 0

        super().save(*args, **kwargs) 

    class Meta:
        verbose_name = _("Tematik reja")
        verbose_name_plural = _("Tematik rejalar")
        unique_together = (
            "quarter",
            "school_type",
            "classes",
            "science",
            "science_language",
        )
        ordering = ("-created_at",)
