from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pedagog.models.download import Download
from apps.pedagog.models.download_token import DownloadToken


@admin.register(Download)
class DownloadAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "date",
        "media",
    )
    autocomplete_fields = ("user", "media")


@admin.register(DownloadToken)
class DownloadTokenAdmin(ModelAdmin):
    list_display = (
        "id",
    )
