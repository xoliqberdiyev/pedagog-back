from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.websocket.models.notification import Notification, FSMToken


@admin.register(Notification)
class NotificationAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "full_name",
        "message",
        "is_read",
        "is_sending",
        "created_at",
    )
    search_fields = (
        "user__first_name",
        "message",
        "user__last_name",
        "user__phone",
    )
    list_filter = ("is_read", "is_sending")
    autocomplete_fields = ("user",)

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")


@admin.register(FSMToken)
class FSMTokenAdmin(ModelAdmin):
    list_display = [
        'user', 'token'
    ]
    search_fields = ['user']