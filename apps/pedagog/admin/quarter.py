from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pedagog.models.quarter import Quarter


@admin.register(Quarter)
class QuarterAdmin(ModelAdmin):
    list_display = (
        "id",
        "choices",
        "start_date",
        "end_date",
    )
    search_fields = ("choices",)
