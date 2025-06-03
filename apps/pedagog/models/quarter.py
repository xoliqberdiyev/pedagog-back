from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.pedagog.models.weeks import Weeks
from apps.shared.models.base import AbstractBaseModel


class Quarter(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4

    QUARTER_CHOICES = [
        (Q1, "First Quarter"),
        (Q2, "Second Quarter"),
        (Q3, "Third Quarter"),
        (Q4, "Fourth Quarter"),
    ]

    choices = models.IntegerField(
        choices=QUARTER_CHOICES,
        default=Q1,
        verbose_name=_("Chorak"),
    )
    start_date = models.DateField(
        default=datetime.today, blank=True, verbose_name=_("Boshlang'ich sana")
    )
    end_date = models.DateField(
        default=datetime.today, blank=True, verbose_name=_("Oxirgi sana")
    )

    def __str__(self):
        return f" {self.choices} ({self.start_date} - {self.end_date})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.get_number_of_weeks()

    def get_number_of_weeks(self):
        delta = self.end_date - self.start_date
        week_count = delta.days // 7

        for i in range(week_count):
            week_start_date = self.start_date + timedelta(weeks=i)
            week_end_date = week_start_date + timedelta(days=6)
            Weeks.objects.get_or_create(
                quarter=self,
                week_count=i + 1,
                defaults={
                    "start_date": week_start_date,
                    "end_date": week_end_date,
                },
            )

    class Meta:
        verbose_name = _("Chorak")
        verbose_name_plural = _("Choraklar")
        ordering = ("-created_at",)
