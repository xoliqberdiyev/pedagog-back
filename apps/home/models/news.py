from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class NewsCategory(AbstractBaseModel):
    """
    Model representing a category for news articles.
    """

    name = models.CharField(
        max_length=255, verbose_name=_("Category Name"), db_index=True
    )

    class Meta:
        verbose_name = _("News Category")
        verbose_name_plural = _("News Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class News(AbstractBaseModel):
    """
    Model representing a news article.
    """

    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.CASCADE,
        related_name="news",
        verbose_name=_("Category"),
        db_index=True,
    )
    reading_time = models.CharField(
        max_length=255,
        verbose_name=_("Reading Time"),
        help_text=_("Estimated reading time for the article."),
        db_index=True,
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"), db_index=True)
    short_title = models.CharField(
        max_length=255, verbose_name=_("Short Title"), db_index=True
    )
    content = models.TextField(
        verbose_name=_("Content"), blank=True, null=True, db_index=True
    )
    image = models.ImageField(
        upload_to="news_images/",
        verbose_name=_("Image"),
        blank=True,
        null=True,
        help_text=_("Upload an image for the news article."),
        db_index=True,
    )
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("View Count"),
        help_text=_("Number of times the article has been viewed."),
        db_index=True,
    )
    is_trending = models.BooleanField(
        default=False,
        verbose_name=_("Is Trending"),
        help_text=_("Indicates if the article is trending."),
        db_index=True,
    )

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def increment_views(self):
        """Ko'rishlar sonini oshirish uchun metod."""
        self.view_count += 1
        self.save(update_fields=["view_count"])


class SeoMetaNewsData(AbstractBaseModel):
    """
    Model representing SEO metadata for a news article.
    """

    news = models.OneToOneField(News, on_delete=models.CASCADE, related_name="seo_meta")
    title = models.CharField(
        max_length=255, verbose_name=_("SEO Title"), blank=True, null=True
    )
    description = models.TextField(
        verbose_name=_("SEO Description"), blank=True, null=True
    )
    keywords = models.CharField(
        max_length=255, verbose_name=_("SEO Keywords"), blank=True, null=True
    )
    canonical_url = models.URLField(
        verbose_name=_("Canonical URL"),
        blank=True,
        null=True,
        help_text=_("Specify the canonical URL for SEO."),
    )

    class Meta:
        verbose_name = _("SEO Meta Data")
        verbose_name_plural = _("SEO Meta Data")

    def __str__(self):
        return f"SEO Meta for {self.news.title}"


class SeoOgNewsData(AbstractBaseModel):
    """
    Model representing Open Graph metadata for a news article.
    """

    news = models.OneToOneField(News, on_delete=models.CASCADE, related_name="og_meta")
    og_title = models.CharField(
        max_length=255, verbose_name=_("OG Title"), blank=True, null=True
    )
    og_description = models.TextField(
        verbose_name=_("OG Description"), blank=True, null=True
    )
    og_image = models.ImageField(
        upload_to="og_images/",
        verbose_name=_("OG Image"),
        blank=True,
        null=True,
        help_text=_("Upload an image for Open Graph."),
    )

    class Meta:
        verbose_name = _("Open Graph Meta Data")
        verbose_name_plural = _("Open Graph Meta Data")

    def __str__(self):
        return f"Open Graph Meta for {self.news.title}"


class SeoTwitterNewsData(AbstractBaseModel):
    """
    Model representing Twitter Card metadata for a news article.
    """

    news = models.OneToOneField(
        News, on_delete=models.CASCADE, related_name="twitter_meta"
    )
    twitter_card = models.CharField(
        max_length=255, verbose_name=_("Twitter Card"), blank=True, null=True
    )
    twitter_title = models.CharField(
        max_length=255, verbose_name=_("Twitter Title"), blank=True, null=True
    )
    twitter_description = models.TextField(
        verbose_name=_("Twitter Description"), blank=True, null=True
    )
    twitter_image = models.ImageField(
        upload_to="twitter_images/",
        verbose_name=_("Twitter Image"),
        blank=True,
        null=True,
        help_text=_("Upload an image for Twitter Card."),
    )

    class Meta:
        verbose_name = _("Twitter Card Meta Data")
        verbose_name_plural = _("Twitter Card Meta Data")

    def __str__(self):
        return f"Twitter Card Meta for {self.news.title}"
