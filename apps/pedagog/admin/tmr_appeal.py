from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import display

from apps.pedagog.models.tmr_appeal import TMRAppeal, TMRAppealStatus, TmrFiles


@admin.register(TMRAppeal)
class TMRAppealAdmin(ModelAdmin):
    list_display = [
        "id",
        "user",
        "show_status_customized_color",
        "school_type",
        "classes",
        "science",
        "science_language",
        "docs_links",
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__father_name",
    ]
    list_filter = [
        "status",
        "school_type",
        "classes",
        "science",
        "science_language",
    ]
    readonly_fields = (
        "user",
        "school_type",
        "classes",
        "science",
        "science_language",
        "created_at",
        "updated_at",
    )

    @display(
        description="Status",
        ordering="status",
        label={
            TMRAppealStatus.ACCEPTED: "success",  # green
            TMRAppealStatus.PENDING: "warning",  # orange
            TMRAppealStatus.REJECTED: "danger",  # red
        },
    )
    def show_status_customized_color(self, obj):
        return obj.status, obj.get_status_display()

    def docs_links(self, obj):
        links = [
            format_html(
                '<a href="{}" target="_blank">{}</a><br>',
                doc.file.url,
                doc.title,
            )
            for doc in obj.files.all()
        ]
        return format_html("<br>".join(links))

    docs_links.short_description = _("Fayllar")


@admin.register(TmrFiles)
class TmrFilesAdmin(ModelAdmin):
    list_display = ("id", "title", "description", "file", "type", "size")
    search_fields = ("title", "description", "file", "type")
    list_filter = ("is_active", "type")
    readonly_fields = ("size", "type")
    autocomplete_fields = ("tmr_appeal",)
