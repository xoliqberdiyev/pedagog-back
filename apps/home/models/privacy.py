from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class PrivacyPolicy(AbstractBaseModel):
    """
    Model to store the privacy policy of the application.
    """

    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("Title of the privacy policy."),
    )
    content = models.TextField(
        verbose_name=_("Content"),
        help_text=_("Content of the privacy policy."),
    )

    class Meta:
        verbose_name = _("Privacy Policy")
        verbose_name_plural = _("Privacy Policies")
        ordering = ("-created_at",)

    def __str__(self):
        return self.title
