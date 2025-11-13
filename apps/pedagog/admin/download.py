from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pedagog.models.download import Download
from apps.pedagog.models.download_token import DownloadToken
from apps.pedagog.models.telegram_message import TelegramMessage



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


@admin.register(TelegramMessage)
class TelegramMessageAdmin(ModelAdmin):
    list_display = (
        "id",
        "chat_id",
        "message_id",
    )