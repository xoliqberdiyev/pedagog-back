from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from apps.pedagog.models.moderator import Moderator


@admin.register(Moderator)
class ModeratorAdmin(ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "is_contracted",
        "degree",
        "docs_links",
        "contract_links",
        "send_contract",
        "status",
    )
    search_fields = ("user__first_name", "user__last_name", "user__phone")
    filter_horizontal = (
        "resource_type",
        "school_type",
        "classes",
        "science",
        "science_language",
        "quarters",
    )
    list_filter = (
        "is_contracted",
        "degree",
        "status",
    )
    ordering = ("-updated_at",)
    readonly_fields = ("docs_links", "balance")
    autocomplete_fields = ("user",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "balance",
                    "paid_amount",
                    "degree",
                    "is_contracted",
                    "docs_links",
                    "card_number",
                    "prosend",
                )
            },
        ),
        (
            _("Plan Permissions"),
            {
                "classes": ["tab"],
                "fields": (
                    "plan_creatable",
                    "school_type",
                    "classes",
                    "science",
                    "science_language",
                    "quarters",
                ),
            },
        ),
        (
            _("Resource Permissions"),
            {
                "classes": ["tab"],
                "fields": (
                    "resource_creatable",
                    "resource_type",
                ),
            },
        ),
        (
            _("topic Permissions"),
            {"classes": ["tab"], "fields": ("topic_creatable",)},
        ),
    )

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def docs_links(self, obj):
        links = [
            format_html(
                '<a href="{}" target="_blank">{}</a><br>',
                doc.file.url,
                doc.title,
            )
            for doc in obj.docs.all()
        ]
        return format_html("<br>".join(links))

    docs_links.short_description = _("Hujjatlar")

    def contract_links(self, obj):
        links = [
            format_html(
                '<a href="{}" target="_blank">{}</a><br>',
                doc.file.url,
                doc.title,
            )
            for doc in obj.user.document.all()
        ]
        return format_html("<br>".join(links))

    contract_links.short_description = _("Kelgan shartnoma")

    def send_contract(self, obj):
        if obj.user.response_file and hasattr(obj.user.response_file, "url"):
            links = [
                format_html(
                    '<a href="{}" target="_blank">{}</a><br>',
                    obj.user.response_file.url,
                    _("Shartnoma"),
                )
            ]
            return format_html("<br>".join(links))
        return _("No contract available")

    send_contract.short_description = _("Tasdiqlangan shartnoma")
