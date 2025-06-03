from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline
from unfold.admin import StackedInline, ModelAdmin

from apps.home.forms.news import NewsForm
from apps.home.models.news import (
    NewsCategory,
    SeoMetaNewsData,
    SeoOgNewsData,
    SeoTwitterNewsData,
    News,
)


@admin.register(NewsCategory)
class NewsCategoryAdmin(ModelAdmin, TabbedTranslationAdmin):
    """
    Админка для управления категориями новостей.
    """

    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("-created_at",)
    list_filter = ("created_at",)
    list_per_page = 20
    date_hierarchy = "created_at"


@admin.register(SeoMetaNewsData)
class SeoMetaNewsDataAdmin(ModelAdmin, TabbedTranslationAdmin):
    """
    Админка для управления SEO Meta данными.
    """

    list_display = ("news", "title", "description", "keywords")
    search_fields = ("news__title", "title", "description", "keywords")
    list_filter = ("news__created_at",)
    ordering = ("-news__created_at",)


@admin.register(SeoOgNewsData)
class SeoOgNewsDataAdmin(ModelAdmin, TabbedTranslationAdmin):
    """
    Админка для управления Open Graph Meta данными.
    """

    list_display = ("news", "og_title", "og_description")
    search_fields = ("news__title", "og_title", "og_description")
    list_filter = ("news__created_at",)
    ordering = ("-news__created_at",)


@admin.register(SeoTwitterNewsData)
class SeoTwitterNewsDataAdmin(ModelAdmin, TabbedTranslationAdmin):
    """
    Админка для управления Twitter Card Meta данными.
    """

    list_display = ("news", "twitter_title", "twitter_description")
    search_fields = ("news__title", "twitter_title", "twitter_description")
    list_filter = ("news__created_at",)
    ordering = ("-news__created_at",)


class SeoMetaNewsDataInline(StackedInline, TranslationStackedInline):
    """
    Inline для управления SEO Meta данными.
    """

    model = SeoMetaNewsData
    extra = 1
    tab = True


class SeoOgNewsDataInline(StackedInline, TranslationStackedInline):
    """
    Inline для управления Open Graph Meta данными.
    """

    model = SeoOgNewsData
    extra = 1
    tab = True


class SeoTwitterNewsDataInline(StackedInline, TranslationStackedInline):
    """
    Inline для управления Twitter Card Meta данными.
    """

    model = SeoTwitterNewsData
    extra = 1
    tab = True


@admin.register(News)
class NewsAdmin(ModelAdmin, TabbedTranslationAdmin):
    """
    Админка для управления новостями.
    """

    list_display = ("title", "short_title", "created_at")
    search_fields = ("title", "short_title")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    autocomplete_fields = ("category",)
    form = NewsForm
    inlines = [SeoMetaNewsDataInline, SeoOgNewsDataInline, SeoTwitterNewsDataInline]
