from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pedagog.models.documents import Document


@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    list_display = ("id", "title", "description", "file", "type", "size")
    search_fields = ("title", "description", "file", "type")
    list_filter = ("is_active", "type")
    readonly_fields = ("size", "type")
    autocomplete_fields = ("user",)
