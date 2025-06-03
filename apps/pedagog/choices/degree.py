from django.db import models
from django.utils.translation import gettext_lazy as _


class Degree(models.TextChoices):
    HIGHER = "HIGHER", _("Oliy toifa")
    EXCELLENT = "EXCELLENT", _("Xalq ta'limi a'lochisi")
    GOOD_TEACHER = "GOOD_TEACHER", _(
        "\"Eng yaxshi o'qituvchi\" konkursi g'olibi"
    )  # noqa
    AUTHOR = "AUTHOR", _("Darslik muallifi")
    POPULAR = "POPULAR", _("Ommlashtirilgan")
    METHODIST = "METHODIST", _("Metodist")
