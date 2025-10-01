from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel
from apps.users.models.user import User


class Notification(AbstractBaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Foydalanuvchi"),
    )
    title = models.CharField(
        max_length=255, verbose_name=_("Sarlavha"), blank=True, null=True
    )
    message = models.TextField(verbose_name=_("Xabar"))
    image = models.ImageField(
        upload_to="notifications/images/",
        verbose_name=_("Rasm"),
        blank=True,
        null=True,
    )
    is_read = models.BooleanField(default=False, verbose_name=_("O'qilgan"))
    is_sending = models.BooleanField(default=False, verbose_name=_("Jo'natilmoqda"))

    def __str__(self) -> str:
        return f"{self.user.phone} | {self.message}"

    class Meta:
        db_table = "notification"
        verbose_name = _("Bildirishnoma")
        verbose_name_plural = _("Bildirishnomalar")
        ordering = ["-created_at"]


class FSMToken(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    token = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'{self.user} - {self.token[:20]}'