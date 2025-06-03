from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class SeoType(models.TextChoices):
    """
    Enum for SEO types.
    """

    HOMEPAGE = "HOMEPAGE", _("Homepage")
    RESOURCE = "RESOURCE", _("Resource")
    NEWS = "NEWS", _("News")
    BLOG = "BLOG", _("Blog")
    PRICE = "PRICE", _("Price")
    CONTACT = "CONTACT", _("Contact")
    POPULAR_NEWS = "POPULAR_NEWS", _("Popular News")
    TRENDING_NEWS = "TRENDING_NEWS", _("Trending News")


class Seo(AbstractBaseModel):
    """
    Model to store SEO information for a page.
    """

    seo_type = models.CharField(
        max_length=20,
        choices=SeoType.choices,
        default=SeoType.HOMEPAGE,
        verbose_name=_("SEO Type"),
        help_text=_("The type of the page for SEO."),
        db_index=True,
    )
    image = models.ImageField(
        upload_to="seo/",
        verbose_name=_("Image"),
        help_text=_("The image for the page for SEO."),
        blank=True,
        null=True,
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("The title of the page for SEO."),
        db_index=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("The description of the page for SEO."),
        db_index=True,
    )
    keywords = models.CharField(
        max_length=255,
        verbose_name=_("Keywords"),
        help_text=_("The keywords for the page for SEO."),
        db_index=True,
    )
    opengraph_title = models.CharField(
        max_length=255,
        verbose_name=_("OpenGraph Title"),
        help_text=_("The OpenGraph title of the page for SEO."),
        db_index=True,
    )
    opengraph_description = models.TextField(
        verbose_name=_("OpenGraph Description"),
        help_text=_("The OpenGraph description of the page for SEO."),
        db_index=True,
    )
    twitter_title = models.CharField(
        max_length=255,
        verbose_name=_("Twitter Title"),
        help_text=_("The Twitter title of the page for SEO."),
        db_index=True,
    )
    twitter_description = models.TextField(
        verbose_name=_("Twitter Description"),
        help_text=_("The Twitter description of the page for SEO."),
        db_index=True,
    )

    class Meta:
        verbose_name = _("SEO")
        verbose_name_plural = _("SEOs")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}"
