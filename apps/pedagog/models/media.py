from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.pedagog.models.topic import Topic
from apps.shared.models.base import AbstractBaseModel


class Media(AbstractBaseModel):
    topic_id = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="medias",
        verbose_name=_("Mavzu"),
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to="media/images/",
        blank=True,
        null=True,
        verbose_name=_("Rasm"),
    )
    name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Nomi")
    )
    desc = models.TextField(blank=True, null=True, verbose_name=_("Tavsif"))
    file = models.FileField(upload_to="media/", verbose_name=_("Fayl"))
    type = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Fayl turi")
    )
    size = models.BigIntegerField(
        blank=True, null=True, default=0, verbose_name=_("Hajmi")
    )
    download_users = models.ManyToManyField(
        "users.User",
        related_name="downloaded_media",
        blank=True,
        verbose_name=_("Yuklab olganlar"),
    )
    count = models.IntegerField(default=0, verbose_name=_("Yuklashlar soni"))
    statistics = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Statistika"),
        default="0%",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="media",
        verbose_name=_("Foydalanuvchi"),
        null=True,
        blank=True,
    )
    object_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Object turi"),
        default="plan",
    )
    object_id = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Object turi ID")
    )
    view_count = models.PositiveIntegerField(
        null=True, blank=True, default=0, verbose_name=_("Ko'rishlar soni")
    )

    def calculation_view_count(self):
        if self.view_count is None:
            self.view_count = 0
        self.view_count += 1
        self.save()

    def __str__(self) -> str:
        return str(self.name) if self.name is not None else f"Media {self.id}"

    def save(self, *args, **kwargs):
        if self.type is None and self.file is not None:
            self.type = self.file.name.split(".")[-1] if "." in self.file.name else None
            self.size = self.file.size if self.file.size is not None else 0
        if self.name is None:
            self.name = (
                self.file.name if self.file.name is not None else f"Media {self.id}"
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Medialar")
        ordering = ("-created_at",)
