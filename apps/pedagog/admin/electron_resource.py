from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline
from unfold.admin import ModelAdmin, StackedInline

from apps.pedagog.models.electron_resource import (
    SeoMetaCategoryData,
    SeoOgCategoryData,
    SeoTwitterCategoryData,
    ElectronResourceCategory,
    ElectronResourceSubCategory,
    ElectronResource,
)


class SeoMetaCategoryDataInline(StackedInline, TranslationStackedInline):
    """
    Inline for managing SEO Meta data.
    """

    model = SeoMetaCategoryData
    extra = 1
    tab = True


class SeoOgCategoryDataInline(StackedInline, TranslationStackedInline):
    """
    Inline for managing Open Graph Meta data.
    """

    model = SeoOgCategoryData
    extra = 1
    tab = True


class SeoTwitterCategoryDataInline(StackedInline, TranslationStackedInline):
    """
    Inline for managing Twitter Card Meta data.
    """

    model = SeoTwitterCategoryData
    extra = 1
    tab = True


@admin.register(ElectronResourceCategory)
class ElectronResourceCategoryAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")
    inlines = (
        SeoTwitterCategoryDataInline,
        SeoOgCategoryDataInline,
        SeoMetaCategoryDataInline,
    )


@admin.register(ElectronResourceSubCategory)
class ElectronResourceSubCategoryAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "description", "category")
    search_fields = ("name", "description", "category__name")
    autocomplete_fields = ("category", "user")


@admin.register(ElectronResource)
class ElectronResourceAdmin(ModelAdmin):
    list_display = ("id", "name", "description", "category")
    search_fields = ("name", "description", "category__name")
    autocomplete_fields = ("category", "user")
    readonly_fields = ("name", "type", "size", "created_at")
