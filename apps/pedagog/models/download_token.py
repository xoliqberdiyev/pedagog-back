import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class DownloadToken(AbstractBaseModel):
    token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_("Token"),
    )
    download = models.ForeignKey(
        "Download", on_delete=models.CASCADE, verbose_name=_("Yuklama")
    )
    expires_at = models.DateTimeField(verbose_name=_("Muddati"))

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return str(self.token)

    class Meta:
        verbose_name = _("Yuklash uchun token")
        verbose_name_plural = _("Yuklash uchun tokenlar")
        ordering = ("-created_at",)
