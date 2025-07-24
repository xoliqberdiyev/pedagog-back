from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.pedagog.models.converted_media import ConvertedMedia


class ConvertedMediaInline(TabularInline):
    model = ConvertedMedia
    extra = 0


@admin.register(ConvertedMedia)
class ConvertedMediaAdmin(ModelAdmin):
    list_display = (
        "id",
        "media",
        "image",
        "page_number",
    )