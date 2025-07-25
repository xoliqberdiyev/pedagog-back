from django.contrib import admin 

from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.pedagog.models.media import MediaType


@admin.register(MediaType)
class MediaTypeAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ['id', 'name_uz', 'name_ru', 'name_en', 'name_ko']