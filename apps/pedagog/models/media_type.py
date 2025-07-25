from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class MediaType(AbstractBaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'media type' 
        verbose_name = 'media types'
        ordering = ('created_at',)