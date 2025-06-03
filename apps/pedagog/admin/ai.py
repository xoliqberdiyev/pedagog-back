from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pedagog.models.ai import Ai


@admin.register(Ai)
class AiAdmin(ModelAdmin):
    list_display = ("id", "topic", "user", "question", "answer")
    search_fields = (
        "topic__name",
        "user__first_name",
        "user__last_name",
        "question",
        "answer",
    )
    autocomplete_fields = ("topic", "user")
