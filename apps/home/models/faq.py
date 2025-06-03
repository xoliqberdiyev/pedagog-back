from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class FAQ(AbstractBaseModel):
    question = models.TextField(verbose_name=_("Savol"))
    answer = models.TextField(verbose_name=_("Javob"))

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ("-created_at",)

    def __str__(self):
        return self.question
