from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.home.models.seo import Seo


@admin.register(Seo)
class SeoAdmin(TabbedTranslationAdmin, ModelAdmin):
    """
    Admin interface for the Seo model.
    """

    list_display = ("id", "seo_type", "title", "keywords", "created_at")
    search_fields = ("title", "description", "keywords")
    list_filter = ("seo_type",)
    ordering = ("-created_at",)
