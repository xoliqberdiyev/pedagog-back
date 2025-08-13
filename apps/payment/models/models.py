from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.pedagog.models.classes import Classes
from apps.pedagog.models.moderator import Moderator
from apps.pedagog.models.quarter import Quarter
from apps.pedagog.models.science import Science, ScienceLanguage
from apps.shared.models.base import AbstractBaseModel
from apps.payment.enums.payment import PaymentType


class Orders(AbstractBaseModel):
    """Order Model"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("Foydalanuvchi"),
    )
    start_date = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name=_("Boshlanish sanasi"),
    )
    end_date = models.DateField(blank=True, null=True, verbose_name=_("Tugash sanasi"))
    classes = models.ForeignKey(
        Classes,
        on_delete=models.CASCADE,
        verbose_name=_("Sinf"),
        related_name="orders",
    )
    science = models.ForeignKey(
        Science,
        on_delete=models.CASCADE,
        verbose_name=_("Fan"),
        related_name="orders",
    )
    science_language = models.ForeignKey(
        ScienceLanguage,
        on_delete=models.CASCADE,
        verbose_name=_("Fan tili"),
        related_name="orders",
        null=True,
        blank=True,
    )
    quarter = models.ForeignKey(
        Quarter,
        on_delete=models.CASCADE,
        verbose_name=_("Chorak"),
        related_name="orders",
    )
    price = models.BigIntegerField(default=0, verbose_name=_("Narxi"))
    status = models.BooleanField(default=False, verbose_name=_("Holati"))

    class Meta:
        verbose_name = _("Buyurtmalar")
        verbose_name_plural = _("Buyurtmalar")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.id} - Incomplete User Information"

    def save(self, *args, **kwargs):
        self.price = Plans.objects.filter(quarter=self.quarter).first().price
        super().save(*args, **kwargs)


class Payments(AbstractBaseModel):
    order = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Buyurtma"),
    )
    price = models.BigIntegerField(default=0, verbose_name=_("Narxi"))
    status = models.BooleanField(default=False, verbose_name=_("Holati"))
    trans_id = models.CharField(
        max_length=255, unique=True, verbose_name=_("Tranzaksiya ID")
    )

    class Meta:
        verbose_name = _("Payments")
        verbose_name_plural = _("Payments")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.id} - Incomplete User Information"


class Plans(AbstractBaseModel):
    quarter = models.ForeignKey(
        Quarter, on_delete=models.CASCADE, verbose_name=_("Chorak")
    )
    price = models.BigIntegerField(default=0, verbose_name=_("Narxi"))
    icon = models.CharField(
        max_length=255,
        verbose_name=_("Icon"),
        null=True,
        blank=True,
        help_text=_("Icon name from Font Awesome"),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Reja nomi"),
        null=True,
        blank=True,
        help_text=_("Plan name"),
    )
    description = models.TextField(
        verbose_name=_("Tavsif"),
        null=True,
        blank=True,
        help_text=_("Description of the plan"),
    )

    class Meta:
        verbose_name = _("Reja")
        verbose_name_plural = _("Rejalar")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.price}"


class PlansRequirements(AbstractBaseModel):
    plan = models.ForeignKey(
        Plans,
        on_delete=models.CASCADE,
        related_name="requirements",
        verbose_name=_("Reja"),
    )
    name = models.CharField(
        max_length=255, verbose_name=_("Talab"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("Reja talabi")
        verbose_name_plural = _("Reja talablar")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.plan} - {self.name}"


class TransactionModel(AbstractBaseModel):
    TransactionStatus = (
        ("pending", "pending"),
        ("success", "success"),
        ("error", "error"),
    )
    transaction_id = models.CharField(
        max_length=255, verbose_name="Transaction ID", null=True, blank=True
    )
    status = models.CharField(
        max_length=100,
        choices=TransactionStatus,
        default="pending",
        verbose_name="status",
    )
    moderator = models.ForeignKey(
        Moderator,
        on_delete=models.CASCADE,
        verbose_name=_("moderator"),
    )

    error = models.TextField(verbose_name="error", null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Amount", default=0.00
    )
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.status} - {self.moderator}"

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ("-create_at",)
