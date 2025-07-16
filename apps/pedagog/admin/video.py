from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.pedagog.models.video import VideoModel


@admin.register(VideoModel)
class BannerAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = [
        "id",
        "title",
        "duration",
    ]
