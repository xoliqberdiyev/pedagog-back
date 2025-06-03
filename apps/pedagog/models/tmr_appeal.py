from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.pedagog.models.classes import Classes
from apps.pedagog.models.school import SchoolType
from apps.pedagog.models.science import ScienceLanguage, Science
from apps.shared.models.base import AbstractBaseModel


class TMRAppealStatus(models.TextChoices):
    PENDING = "pending", _("Kutilmoqda")
    ACCEPTED = "accepted", _("Qabul qilindi")
    REJECTED = "rejected", _("Rad etildi")


class TMRAppeal(AbstractBaseModel):
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        verbose_name=_("Foydalanuvchi"),
    )
    status = models.CharField(
        max_length=20,
        choices=TMRAppealStatus.choices,
        default=TMRAppealStatus.PENDING,
        verbose_name=_("Holat"),
    )
    school_type = models.ForeignKey(
        SchoolType,
        on_delete=models.CASCADE,
        verbose_name=_("Maktab turi"),
        related_name="tmr_appeals",
        null=True,
        blank=True,
    )
    classes = models.ForeignKey(
        Classes,
        on_delete=models.CASCADE,
        verbose_name=_("Sinf"),
        related_name="tmr_appeals",
    )
    science = models.ForeignKey(
        Science,
        on_delete=models.CASCADE,
        verbose_name=_("Fan"),
        related_name="tmr_appeals",
    )
    science_language = models.ForeignKey(
        ScienceLanguage,
        on_delete=models.CASCADE,
        verbose_name=_("Fan tili"),
        related_name="tmr_appeals",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user} - {self.status}"

    class Meta:
        verbose_name = _("TMR arizalari")
        verbose_name_plural = _("TMR arizalari")
        ordering = ("-created_at",)

    @classmethod
    def get_pending(cls):
        return cls.objects.filter(status=TMRAppealStatus.PENDING).count()


class TmrFiles(AbstractBaseModel):
    tmr_appeal = models.ForeignKey(
        "TMRAppeal",
        on_delete=models.CASCADE,
        verbose_name=_("TMR"),
        related_name="files",
    )
    title = models.CharField(_("Nomi"), max_length=255, blank=True, null=True)
    description = models.TextField(_("Tasnifi"), blank=True, null=True)
    file = models.FileField(_("Fayl"), upload_to="tmr/%Y/%m/%d/")
    is_active = models.BooleanField(_("Holati"), default=True)
    type = models.CharField(_("Turi"), max_length=255, blank=True, null=True)
    size = models.BigIntegerField(_("Hajmi"), blank=True, null=True, default=0)

    class Meta:
        verbose_name = _("Tmr Fayllari")
        verbose_name_plural = _("Tmr Fayllari")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} - {self.file.name} - {self.type}"

    def save(self, *args, **kwargs):
        self.type = self.file.name.split(".")[-1]
        self.size = self.file.size
        if self.title is None:
            self.title = (
                self.file.name if self.file.name is not None else f"Media {self.id}"
            )
            self.description = f"{self.title}"
        super().save(*args, **kwargs)

    @property
    def url(self):
        return self.file.url
