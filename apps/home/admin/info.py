from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.home.models.info import PedagogInfo


@admin.register(PedagogInfo)
class PedagogInfoAdmin(TabbedTranslationAdmin, ModelAdmin):
    """
    Admin view for PedagogInfo model.
    """

    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title",)
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)
