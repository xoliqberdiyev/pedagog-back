from django.db import models
from django.utils.translation import gettext_lazy as _


class VideoModel(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    desc = models.TextField(_("Desc"))
    duration = models.PositiveIntegerField(_("Duration"))
    video = models.URLField(_("Video link"))
    badge_title = models.CharField(_("badge title"), max_length=255)
    badge_color = models.CharField(_("badge color"), max_length=255)
