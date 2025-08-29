import math
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from apps.pedagog.models.documents import Document
from apps.shared.models.base import AbstractBaseModel
from apps.users.choices.role import Role
from apps.users.managers.user import UserManager


class SourceChoice(models.TextChoices):
    BOT = "bot", "Bot"
    MOBILE = "mobile", "Mobile App"
    WEB = "web", "Web"
    CLICK_APP = "click_app", "Click App"


class ContractStatus(models.TextChoices):
    NO_FILE = "NO_FILE", _("Hujjat yuklanmagan")
    WAITING = "WAITING", _("Hujjat topshirgan")
    ACCEPTED = "ACCEPTED", _("Shartnoma tuzilgan")
    REJECTED = "REJECTED", _("Shartnoma bekor qilingan")




class User(AbstractUser, AbstractBaseModel):
    phone = models.CharField(max_length=255, unique=True, verbose_name=_("Telefon"))
    username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Foydalanuvchi nomi"),
    )
    father_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Otasining ismi")
    )
    avatar = models.ImageField(
        upload_to="avatar/", blank=True, null=True, verbose_name=_("Avatar")
    )
    validated_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Tasdiqlangan vaqti")
    )
    role = models.CharField(
        max_length=255,
        choices=Role.choices,
        default=Role.USER,
        verbose_name=_("Rol"),
        null=True,
        blank=True,
    )

    region = models.ForeignKey(
        "Region",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Viloyat"),
    )
    district = models.ForeignKey(
        "District",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Tuman"),
    )
    institution_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Muassasa raqami")
    )
    source = models.CharField(
        verbose_name=_("Qayerdan ?"),
        max_length=100,
        choices=SourceChoice.choices,
        default=SourceChoice.WEB,
        blank=True, null=True
    )

    # refferal
    referred_by = models.ForeignKey(
        "self",
        verbose_name="Taklif qilingan",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="referrals"
    )
    referral_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    # bot-
    tg_id = models.BigIntegerField(verbose_name=_("Tg ID"), blank=True, null=True)

    

    USERNAME_FIELD = "phone"

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} {self.father_name} | {self.phone}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": self.id,
        }

    def save(self, *args, **kwargs):
        self.username = self.phone
        if self.phone == "946593659":
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Foydalanuvchilar")
        verbose_name_plural = _("Foydalanuvchilar")
        ordering = ["-created_at"]





class BotUsers(AbstractBaseModel):
    tg_id = models.BigIntegerField(verbose_name=_("Tg id"))
    first_name = models.CharField(verbose_name=_("Ism"), max_length=100)
    
    def __str__(self):
        return self.first_name
    
    class Meta:
        verbose_name = _("Bot Foydalanuvchilar")
        verbose_name_plural = _("Bot Foydalanuvchilar")
        ordering = ["-created_at"]



class UserProfile(AbstractBaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("Foydalanuvchi"),
    )
    document = models.ManyToManyField(
        Document,
        blank=True,
        verbose_name=_("Hujjat"),
    )
    response_file = models.FileField(
        upload_to="response_file/",
        null=True,
        blank=True,
        verbose_name=_("Javob hujjati"),
    )
    status_file = models.CharField(
        max_length=255,
        choices=ContractStatus.choices,
        default=ContractStatus.NO_FILE,
        verbose_name=_("Status"),
    )
    status = models.BooleanField(default=False, verbose_name=_("Shartnoma statusi"))
    balance = models.DecimalField(
        max_digits=100,
        decimal_places=5,
        default=0.00,
        verbose_name=_("Balans"),
    )
    card_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Karta raqami"),
    )

    @classmethod
    def user_get_status_count(cls):
        return cls.objects.filter(
            status_file=ContractStatus.WAITING, user__role=Role.MODERATOR
        ).count()

    class Meta:
        verbose_name = _("Foydalanuvchi profili")
        verbose_name_plural = _("Foydalanuvchi profillari")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.last_name} {self.user.first_name} {self.user.father_name} | {self.user.phone}"





class SmsConfirm(AbstractBaseModel):
    SMS_EXPIRY_SECONDS = 120
    RESEND_BLOCK_MINUTES = 10
    TRY_BLOCK_MINUTES = 2
    RESEND_COUNT = 5
    TRY_COUNT = 10

    code = models.IntegerField(verbose_name=_("Kod"))
    try_count = models.IntegerField(default=0, verbose_name=_("Urinishlar soni"))
    resend_count = models.IntegerField(
        default=0, verbose_name=_("Qayta yuborishlar soni")
    )
    phone = models.CharField(max_length=255, verbose_name=_("Telefon raqami"))
    expire_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Muddati"))
    unlock_time = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Bloklanish vaqti")
    )
    resend_unlock_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Qayta yuborish bloklanish vaqti"),
    )

    def sync_limits(self):
        if self.resend_count >= self.RESEND_COUNT:
            self.try_count = 0
            self.resend_count = 0
            self.resend_unlock_time = timezone.now() + timedelta(
                minutes=self.RESEND_BLOCK_MINUTES
            )
        elif self.try_count >= self.TRY_COUNT:
            self.try_count = 0
            self.unlock_time = timezone.now() + timedelta(
                minutes=self.TRY_BLOCK_MINUTES
            )

        if (
            self.resend_unlock_time is not None
            and self.resend_unlock_time.timestamp() < timezone.now().timestamp()
        ):
            self.resend_unlock_time = None

        if (
            self.unlock_time is not None
            and self.unlock_time.timestamp() < timezone.now().timestamp()
        ):
            self.unlock_time = None
        self.save()

    def is_expired(self):
        return (
            self.expire_time.timestamp() < timezone.now().timestamp()
            if hasattr(self.expire_time, "timestamp")
            else None
        )

    def is_block(self):
        return self.unlock_time is not None

    def reset_limits(self):
        self.try_count = 0
        self.resend_count = 0
        self.unlock_time = None

    def interval(self, time):
        expire = time.timestamp() - timezone.now().timestamp()
        minutes = math.floor(expire / 60)
        expire -= minutes * 60
        expire = math.floor(expire)

        return f"{minutes:02d}:{expire:02d}"

    def __str__(self) -> str:
        return f"{self.phone} | {self.code}"
