from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class ElectronResourceCategory(AbstractBaseModel):
    """
    Model for storing electron resources.
    """

    class Meta:
        verbose_name = _("Electron Resource")
        verbose_name_plural = _("Electron Resources")
        ordering = ("-created_at",)

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    first_color = models.CharField(
        _("First Color"), max_length=255, blank=True, null=True
    )
    second_color = models.CharField(
        _("Second Color"), max_length=255, blank=True, null=True
    )
    icon = models.CharField(_("Icon"), max_length=255, blank=True, null=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    def __str__(self):
        return self.name


class ElectronResourceSubCategory(AbstractBaseModel):
    """
    Model for storing electron resources.
    """

    class Meta:
        verbose_name = _("Electron Resource Sub Category")
        verbose_name_plural = _("Electron Resource Sub Categories")
        ordering = ("-created_at",)

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    category = models.ForeignKey(
        ElectronResourceCategory,
        on_delete=models.CASCADE,
        related_name="sub_categories",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="sub_categories",
        db_index=True,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(_("Is Active"), default=True)

    def __str__(self):
        return self.name


class ElectronResource(AbstractBaseModel):
    """
    Model for storing electron resources.
    """

    class Meta:
        verbose_name = _("Electron Resource File")
        verbose_name_plural = _("Electron Resource Files")
        ordering = ["-created_at"]
        db_table = "electron_resource_files"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="files",
        db_index=True,
        blank=True,
        null=True,
    )
    description = models.TextField(_("Description"), blank=True, null=True)
    file = models.FileField(_("File"), upload_to="electron_resources/")
    name = models.CharField(_("Name"), max_length=255)
    size = models.CharField(_("Size"), max_length=255, blank=True, null=True)
    type = models.CharField(_("Type"), max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        ElectronResourceSubCategory,
        on_delete=models.CASCADE,
        related_name="resources",
    )
    price = models.PositiveIntegerField(null=True, blank=True)
    preview = models.FileField(
        null=True, blank=True, upload_to='electron_resources/',
    )
    
    is_active = models.BooleanField(_("Is Active"), default=True)

    def __str__(self):
        return str(self.name)

    def get_file_size(self, size=None):
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{round(size / 1024, 2)} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{round(size / (1024 * 1024), 2)} MB"
        else:
            return f"{round(size / (1024 * 1024 * 1024), 2)} GB"

    def get_file_name(self, file=None):
        if file:
            return file.split("/")[-1]
        return file

    def save(self, *args, **kwargs):
        self.size = self.get_file_size(self.file.size)
        self.type = self.file.name.split(".")[-1]
        self.name = self.get_file_name(self.file.name)
        super().save(*args, **kwargs)


class SeoMetaCategoryData(AbstractBaseModel):
    """
    Model representing SEO metadata for a Category article.
    """

    category = models.OneToOneField(
        ElectronResourceCategory, on_delete=models.CASCADE, related_name="seo_meta"
    )
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
        return f"SEO Meta for {self.category.name}"


class SeoOgCategoryData(AbstractBaseModel):
    """
    Model representing Open Graph metadata for a Category article.
    """

    category = models.OneToOneField(
        ElectronResourceCategory, on_delete=models.CASCADE, related_name="og_meta"
    )
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
        return f"Open Graph Meta for {self.category.name}"


class SeoTwitterCategoryData(AbstractBaseModel):
    """
    Model representing Twitter Card metadata for a Category article.
    """

    category = models.OneToOneField(
        ElectronResourceCategory, on_delete=models.CASCADE, related_name="twitter_meta"
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
        return f"Twitter Card Meta for {self.category.name}"
