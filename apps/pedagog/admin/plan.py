from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from apps.pedagog.models.plan import Plan


@admin.register(Plan)
class PlanAdmin(ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "school_type",
        "classes",
        "science",
        "science_language",
        "quarter",
        "created_at",
        "is_active",
    )
    list_editable = ("is_active",)
    list_filter_submit = True
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__phone",
    )
    autocomplete_fields = (
        "user",
        "school_type",
        "classes",
        "science",
        "science_language",
        "quarter",
    )

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")
