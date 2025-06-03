from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class Download(AbstractBaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Foydalanuvchi"),
    )
    date = models.DateField(verbose_name=_("Sanasi"))
    media = models.ForeignKey(
        "Media", on_delete=models.CASCADE, verbose_name=_("Media")
    )
    object_type = models.CharField(
        max_length=255, verbose_name=_("Yuklash turi"), blank=True, null=True
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_("Object ID"), blank=True, null=True
    )

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = _("Yuklamalar")
        verbose_name_plural = _("Yuklamalar")
        ordering = ("-created_at",)
