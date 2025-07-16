from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pedagog.models.video import VideoModel


@admin.register(VideoModel)
class BannerAdmin(ModelAdmin):
    list_display = [
        "id",
        "title",
        "duration",
    ]
