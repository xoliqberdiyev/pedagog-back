from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.home.forms.privacy import PrivacyPolicyForm
from apps.home.models.privacy import PrivacyPolicy


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(ModelAdmin, TabbedTranslationAdmin):
    """
    Admin interface for the PrivacyPolicy model.
    """

    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title",)
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)
    form = PrivacyPolicyForm
