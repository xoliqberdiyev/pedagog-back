from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pedagog.models.weeks import Weeks


@admin.register(Weeks)
class WeeksAdmin(ModelAdmin):
    list_display = ("id", "quarter", "week_count", "start_date", "end_date")
    search_fields = ("quarter__choices", "week_count")
    autocomplete_fields = ("quarter",)
    list_filter = ("quarter",)
