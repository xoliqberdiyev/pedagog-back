"""
Admin panel register
"""

from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.users.models.user import SmsConfirm


@admin.register(SmsConfirm)
class SmsConfirmAdmin(ModelAdmin):
    list_display = ["id", "phone", "code", "resend_count", "try_count"]
    search_fields = ["phone", "code"]
    ordering = ["-created_at"]
