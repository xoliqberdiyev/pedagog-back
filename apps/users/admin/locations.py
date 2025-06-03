from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.users.models.locations import Region, District


@admin.register(Region)
class RegionAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(District)
class DistrictAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "region", "name"]
    search_fields = ["region__name", "name"]
    autocomplete_fields = ["region"]
