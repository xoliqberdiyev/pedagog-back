from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pedagog.models.media import Media


@admin.register(Media)
class MediaAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "file",
        "type",
        "count",
        "statistics",
    )
    search_fields = ("name",)
    list_display_links = ("name",)
    list_filter = ("type", "object_type")
    list_filter_submit = True
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("download_users",)
    autocomplete_fields = ("download_users", "user", "topic_id")
