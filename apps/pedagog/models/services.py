from django.db import models
from django.utils.translation import gettext_lazy as _


class ServicesModel(models.Model):
    title = models.CharField(_("title"))
    logo = models.ImageField(_("image"))
    url = models.URLField(_("url"))
