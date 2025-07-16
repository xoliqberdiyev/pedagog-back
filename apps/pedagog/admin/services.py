from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.pedagog.models.services import ServicesModel


@admin.register(ServicesModel)
class ServicesAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = [
        "id",
        "title",
        "url",
    ]
