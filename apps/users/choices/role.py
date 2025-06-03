from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    ADMIN = "admin", _("Administrator")
    MODERATOR = "moderator", _("Moderator")
    USER = "user", _("Foydalanuvchi")
