from django.db import models
from django.utils.translation import gettext_lazy as _


class BannerModel(models.Model):
    title = models.CharField(_("title"))
    description = models.TextField(_("description"), null=True, blank=True)
    image = models.ImageField(_("image"))

    def __str__(self):
        return self.title

    class Meta:
        db_table = "banners"
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")
