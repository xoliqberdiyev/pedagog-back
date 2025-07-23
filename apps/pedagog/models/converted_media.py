from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel
from apps.pedagog.models.media import Media


class ConvertedMedia(AbstractBaseModel):
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name='converted_medias',
    )
    image = models.ImageField(upload_to='converted_images/')
    page_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.media} - {self.image}"

    class Meta:
        verbose_name = _("O'zgartirilgan media")
        verbose_name_plural = _("O'zgartirilgan media")
        ordering = ("-created_at", "page_number")