from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pedagog.models.schedule import LessonSchedule


@admin.register(LessonSchedule)
class LessonScheduleAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "quarter",
        "shift",
        "classes",
        "class_group",
        "science",
        "science_language",
    )
    search_fields = (
        "user__username",
        "quarter__name",
        "classes__name",
        "science__name",
    )
    list_filter = ("quarter", "shift", "classes", "science")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    autocomplete_fields = (
        "user",
        "quarter",
        "classes",
        "class_group",
        "science",
        "science_language",
    )
    readonly_fields = ("created_at", "updated_at")
