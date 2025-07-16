from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.pedagog.models.banner import BannerModel


@admin.register(BannerModel)
class BannerAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = [
        "title",
        "image",
    ]
