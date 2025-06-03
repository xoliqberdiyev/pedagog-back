from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.payment.services.services import get_user_profit
from apps.pedagog.choices.degree import Degree
from apps.pedagog.models.classes import Classes
from apps.pedagog.models.school import SchoolType
from apps.pedagog.models.science import Science, ScienceLanguage
from apps.shared.models.base import AbstractBaseModel


class Moderator(AbstractBaseModel):
    @property
    def profit(self):
        return get_user_profit(self.user)

    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi")
    )
    balance = models.BigIntegerField(default=0, verbose_name=_("Balans"))
    paid_amount = models.BigIntegerField(default=0, verbose_name=_("To'langan pul"))
    prosend = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name=_("Prosent"),
        blank=True,
        null=True,
    )
    degree = models.CharField(
        max_length=15,
        choices=Degree.choices,
        default=Degree.AUTHOR,
        verbose_name=_("Daraja"),
    )
    card_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_("Karta raqami")
    )
    docs = models.ManyToManyField(
        "Document",
        blank=True,
        related_name="moderators",
        verbose_name=_("Hujjatlar"),
    )
    is_contracted = models.BooleanField(default=False, verbose_name=_("Tasdiqlash"))
    status = models.BooleanField(default=False, verbose_name=_("Shartnoma statusi"))
    plan_creatable = models.BooleanField(
        default=False, verbose_name=_("Tematik Reja yarata olishi")
    )
    resource_creatable = models.BooleanField(
        default=False, verbose_name=_("Resurs yarata olishi.")
    )
    topic_creatable = models.BooleanField(
        default=False, verbose_name=_("Mavzu yarata olishi.")
    )
    resource_type = models.ManyToManyField(
        "ElectronResourceCategory",
        blank=True,
        related_name="moderators",
        verbose_name=_("Resurs turlari"),
    )
    # plan
    school_type = models.ManyToManyField(
        SchoolType,
        blank=True,
        related_name="moderators",
        verbose_name=_("Maktab turi"),
    )
    classes = models.ManyToManyField(
        Classes,
        blank=True,
        related_name="moderators",
        verbose_name=_("Sinf"),
    )
    science = models.ManyToManyField(
        Science,
        blank=True,
        related_name="moderators",
        verbose_name=_("Fan"),
    )
    science_language = models.ManyToManyField(
        ScienceLanguage,
        blank=True,
        related_name="moderators",
        verbose_name=_("Fan tili"),
    )

    quarters = models.ManyToManyField(
        "Quarter",
        blank=True,
        related_name="moderators",
        verbose_name=_("Choraklar"),
    )

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} | {self.user.phone}"

    @classmethod
    def moderator_get_status_count(cls):
        return cls.objects.filter(is_contracted=False).count()

    class Meta:
        verbose_name = _("Moderator")
        verbose_name_plural = _("Moderatorlar")
        ordering = ["-updated_at"]
