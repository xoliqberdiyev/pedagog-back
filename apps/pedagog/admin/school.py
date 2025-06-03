from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.pedagog.models.school import SchoolType


@admin.register(SchoolType)
class SchoolTypeAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "name",
        "created_at",
    )
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    ordering = ("name",)
    autocomplete_fields = ("classes",)
