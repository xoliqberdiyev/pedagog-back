from django.db import models

from apps.pedagog.models.classes import Classes
from apps.pedagog.models.school import SchoolType
from apps.pedagog.models.science import Science, ScienceLanguage
from apps.shared.models.base import AbstractBaseModel
from django.utils.translation import gettext_lazy as _


class ModeratorPermissionStatus(models.TextChoices):
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    PENDING = "pending", "Pending"


class ModeratorPermission(AbstractBaseModel):
    """
    Model to represent a moderator permission.
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="moderator_permissions",
        verbose_name="User",
    )
    status = models.CharField(
        max_length=10,
        choices=ModeratorPermissionStatus.choices,
        default=ModeratorPermissionStatus.PENDING,
        verbose_name="Status",
    )

    school_type = models.ManyToManyField(
        SchoolType,
        blank=True,
        related_name="moderator_permissions",
        verbose_name=_("Maktab turi"),
    )
    classes = models.ManyToManyField(
        Classes,
        blank=True,
        related_name="moderator_permissions",
        verbose_name=_("Sinf"),
    )
    science = models.ManyToManyField(
        Science,
        blank=True,
        related_name="moderator_permissions",
        verbose_name=_("Fan"),
    )
    science_language = models.ManyToManyField(
        ScienceLanguage,
        blank=True,
        related_name="moderator_permissions",
        verbose_name=_("Fan tili"),
    )

    class Meta:
        verbose_name = "Moderator Permission"
        verbose_name_plural = "Moderator Permissions"

    def __str__(self):
        return f"{self.user.phone} - {self.status}"

    @classmethod
    def moderator_get_status_count(cls):
        return cls.objects.filter(status=ModeratorPermissionStatus.PENDING).count()
