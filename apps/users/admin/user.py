from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.admin import StackedInline
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.decorators import display
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

from apps.pedagog.models.moderator import Moderator
from apps.users.models.user import ContractStatus, User


class ModeratorInline(StackedInline):
    model = Moderator
    fields = [
        "balance",
        "degree",
        "docs",
        "is_contracted",
    ]
    readonly_fields = ["balance"]
    autocomplete_fields = ["docs"]


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin, ImportExportModelAdmin):
    change_password_form = AdminPasswordChangeForm
    add_form = UserCreationForm
    form = UserChangeForm
    list_filter_submit = True
    list_display = [
        "id",
        "phone",
        "first_name",
        "last_name",
        "father_name",
        "role",
        "show_status_customized_color",
        "status",
        "created_at",
    ]
    filter_horizontal = ("groups", "user_permissions")
    search_fields = ["phone", "first_name", "last_name", "father_name"]
    readonly_fields = ("docs_links",)
    list_filter = [
        "role",
        "status_file",
        "status",
        ("created_at", RangeDateTimeFilter),
    ]
    inlines = [ModeratorInline]
    autocomplete_fields = [
        "region",
        "district",
        "document",
    ]
    ordering = ["-updated_at"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "phone",
                    "password",
                    "docs_links",
                    "response_file",
                )
            },
        ),
        (
            "Personal info",
            {
                "classes": ["tab"],
                "fields": (
                    "first_name",
                    "last_name",
                    "father_name",
                    "region",
                    "district",
                    "avatar",
                    "institution_number",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ["tab"],
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates",
            {"classes": ["tab"], "fields": ("last_login", "date_joined")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2"),
            },
        ),
    )

    def docs_links(self, obj):
        links = [
            format_html(
                '<a href="{}" target="_blank">{}</a> - {}<br>'
                '<a href="{}" target="_blank">{}</a><br>',
                doc.file.url,
                doc.title,
                _("Aktiv") if doc.is_active else _("Bekor qilingan"),
                doc.response_file.url if doc.response_file else "#",
                (_("Response File") if doc.response_file else _("No Response File")),
            )
            for doc in obj.document.all()
        ]
        return format_html("<br>".join(links))

    docs_links.short_description = _("Hujjatlar")

    @display(
        description="Status",
        ordering="status",
        label={
            ContractStatus.ACCEPTED: "success",  # green
            ContractStatus.NO_FILE: "info",  # orange
            ContractStatus.WAITING: "warning",  # red
            ContractStatus.REJECTED: "danger",  # red
        },
    )
    def show_status_customized_color(self, obj):
        return obj.status_file, obj.get_status_file_display()
