from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.pedagog.models.classes import Classes, ClassGroup
from apps.pedagog.models.quarter import Quarter
from apps.pedagog.models.science import Science, ScienceLanguage
from apps.shared.models.base import AbstractBaseModel


class Shift(models.TextChoices):
    FIRST = "1", _("1-smena")
    SECOND = "2", _("2-smena")


class WeekDay(models.IntegerChoices):
    MONDAY = 0, _("Dushanba")
    TUESDAY = 1, _("Seshanba")
    WEDNESDAY = 2, _("Chorshanba")
    THURSDAY = 3, _("Payshanba")
    FRIDAY = 4, _("Juma")
    SATURDAY = 5, _("Shanba")
    SUNDAY = 6, _("Yakshanba")


class ScheduleType(models.TextChoices):
    FIRST_WEEK = "FIRST_WEEK", _("Birinchi hafta")
    SECOND_WEEK = "SECOND_WEEK", _("Ikkinchi hafta")


class LessonSchedule(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE)
    shift = models.CharField(max_length=1, choices=Shift.choices, default=Shift.FIRST)

    classes = models.ForeignKey(
        Classes,
        on_delete=models.CASCADE,
        verbose_name=_("Sinf"),
        related_name="schedule",
    )
    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.CASCADE,
        verbose_name=_("Sinf guruhi"),
        related_name="schedule",
        null=True,
        blank=True,
    )
    science = models.ForeignKey(
        Science,
        on_delete=models.CASCADE,
        verbose_name=_("Fan"),
        related_name="schedule",
    )
    science_language = models.ForeignKey(
        ScienceLanguage,
        on_delete=models.CASCADE,
        verbose_name=_("Fan tili"),
        related_name="schedule",
        null=True,
        blank=True,
    )

    weekday = models.IntegerField(choices=WeekDay.choices)
    lesson_number = models.PositiveSmallIntegerField()
    color = models.CharField(
        max_length=10,
        default="#FFFFFF",
        help_text=_("Color in hex format, e.g., #FF5733"),
    )
    schedule_type = models.CharField(
        max_length=20,
        choices=ScheduleType.choices,
        default=ScheduleType.FIRST_WEEK,
        verbose_name=_("Reja turi"),
        help_text=_("Reja turi: Birinchi hafta yoki Ikkinchi hafta"),
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["classes", "date", "start_time", "shift"],
                name="unique_schedule_per_class_date_time",
            )
        ]
        ordering = ["weekday", "lesson_number", "start_time"]

    def __str__(self):
        return f"{self.classes} - {self.science} - {self.start_time} - {self.end_time}"
