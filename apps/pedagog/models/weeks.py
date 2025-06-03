from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class Weeks(AbstractBaseModel):
    quarter = models.ForeignKey("Quarter", models.CASCADE, verbose_name=_("Chorak"))
    week_count = models.IntegerField(verbose_name=_("Hafta raqami"))
    start_date = models.DateField(verbose_name=_("Haftaning boshlanish sanasi"))
    end_date = models.DateField(verbose_name=_("Haftaning tugash sanasi"))

    class Meta:
        verbose_name = _("Hafta")
        verbose_name_plural = _("Haftalar")
        ordering = ("-created_at",)

    def __str__(self):
        return f"Week {self.week_count} ({self.start_date} - {self.end_date})"
