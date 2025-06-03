from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pedagog.models.degree import Degree


@admin.register(Degree)
class DegreeAdmin(ModelAdmin):
    """
    Admin interface for managing degrees.
    """

    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
