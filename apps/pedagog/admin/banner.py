from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pedagog.models.banner import BannerModel


@admin.register(BannerModel)
class BannerAdmin(ModelAdmin):
    list_display = [
        "title",
        "image",
    ]
