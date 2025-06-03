from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class BlogCategory(AbstractBaseModel):
    """
    BlogCategory model to store blog categories.
    """

    name = models.CharField(max_length=255, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Blog(AbstractBaseModel):
    """
    Blog model to store blog posts.
    """

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.CASCADE,
        related_name="blogs",
        verbose_name=_("Category"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    short_title = models.CharField(max_length=255, verbose_name=_("Short Title"))
    content = models.TextField(verbose_name=_("Content"))
    image = models.ImageField(
        verbose_name=_("Image"), upload_to="blogs/", blank=True, null=True
    )
    reading_time = models.CharField(
        max_length=255, verbose_name=_("Reading Time"), blank=True, null=True
    )

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class SeoMetaBlogData(AbstractBaseModel):
    """
    Model representing SEO metadata for a Blog article.
    """

    blog = models.OneToOneField(Blog, on_delete=models.CASCADE, related_name="seo_meta")
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
        return f"SEO Meta for {self.blog.title}"


class SeoOgBlogData(AbstractBaseModel):
    """
    Model representing Open Graph metadata for a Blog article.
    """

    blog = models.OneToOneField(Blog, on_delete=models.CASCADE, related_name="og_meta")
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
        return f"Open Graph Meta for {self.blog.title}"


class SeoTwitterBlogData(AbstractBaseModel):
    """
    Model representing Twitter Card metadata for a Blog article.
    """

    blog = models.OneToOneField(
        Blog, on_delete=models.CASCADE, related_name="twitter_meta"
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
        return f"Twitter Card Meta for {self.blog.title}"
