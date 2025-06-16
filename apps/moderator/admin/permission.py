from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.moderator.models.permission import ModeratorPermission


@admin.register(ModeratorPermission)
class ModeratorPermissionAdmin(ModelAdmin):
    """
    Admin interface for ModeratorPermission model.
    """

    list_display = (
        "id",
        "user",
        "status",
        "created_at",
    )
    search_fields = ("user__phone",)
    list_filter = ("status",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    filter_horizontal = ("school_type", "classes", "science", "science_language")
    autocomplete_fields = ("user",)
