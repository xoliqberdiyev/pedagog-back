from django.db import models
from django.utils.translation import gettext_lazy as _


class ServicesModel(models.Model):
    title = models.CharField(_("title"))
    url = models.CharField(_("url"), max_length=1000)
    icon = models.CharField(_("icon"), max_length=255)
    icon_color = models.CharField(_("icon color"), max_length=100)
    desc = models.TextField(_("descirption"))
