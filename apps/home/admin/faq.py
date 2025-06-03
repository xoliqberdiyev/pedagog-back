from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.home.models.faq import FAQ


@admin.register(FAQ)
class FAQAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "question"]
    search_fields = ["question", "answer"]
    list_filter = ["created_at"]
