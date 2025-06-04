from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.pedagog.models.classes import Classes, ClassGroup
from apps.pedagog.models.quarter import Quarter
from apps.pedagog.models.science import Science, ScienceLanguage
from apps.pedagog.models.topic import Topic
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


class LessonSchedule(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE)
    shift = models.CharField(max_length=1, choices=Shift.choices, default=Shift.FIRST)

    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
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

    date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["classes", "date", "start_time"],
                name="unique_schedule_per_class_date_time",
            )
        ]
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.classes} - {self.science} - {self.date} - {self.start_time} - {self.end_time}"
