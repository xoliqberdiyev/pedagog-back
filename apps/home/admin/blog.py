from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline
from unfold.admin import ModelAdmin, StackedInline

from apps.home.forms.blog import BlogForm
from apps.home.models.blog import (
    SeoMetaBlogData,
    SeoOgBlogData,
    SeoTwitterBlogData,
    BlogCategory,
    Blog,
)


class SeoMetaBlogDataInline(StackedInline, TranslationStackedInline):
    """
    Inline for managing SEO Meta data.
    """

    model = SeoMetaBlogData
    extra = 1
    tab = True


class SeoOgBlogDataInline(StackedInline, TranslationStackedInline):
    """
    Inline for managing Open Graph Meta data.
    """

    model = SeoOgBlogData
    extra = 1
    tab = True


class SeoTwitterBlogDataInline(StackedInline, TranslationStackedInline):
    """
    Inline for managing Twitter Card Meta data.
    """

    model = SeoTwitterBlogData
    extra = 1
    tab = True


@admin.register(BlogCategory)
class BlogCategoryAdmin(ModelAdmin, TabbedTranslationAdmin):
    """
    Admin interface for BlogCategory model.
    """

    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("-created_at",)
    list_filter = ("created_at",)
    list_per_page = 20
    date_hierarchy = "created_at"


@admin.register(Blog)
class BlogAdmin(ModelAdmin, TabbedTranslationAdmin):
    """
    Admin interface for Blog model.
    """

    list_display = ("title", "category", "created_at", "updated_at")
    search_fields = ("title", "category__name")
    ordering = ("-created_at",)
    list_filter = ("category", "created_at")
    list_per_page = 20
    autocomplete_fields = ("category",)
    form = BlogForm
    inlines = [SeoMetaBlogDataInline, SeoOgBlogDataInline, SeoTwitterBlogDataInline]


@admin.register(SeoMetaBlogData)
class SeoMetaBlogDataAdmin(ModelAdmin, TabbedTranslationAdmin):
    """
    Admin interface for SeoMetaBlogData model.
    """

    list_display = ("blog", "title", "description", "keywords", "canonical_url")
    search_fields = ("blog__title", "title", "description", "keywords")
    ordering = ("-created_at",)
    list_filter = ("blog__category",)
    list_per_page = 20
    date_hierarchy = "created_at"


@admin.register(SeoOgBlogData)
class SeoOgBlogDataAdmin(ModelAdmin, TabbedTranslationAdmin):
    """
    Admin interface for SeoOgBlogData model.
    """

    list_display = ("blog", "og_title", "og_description", "og_image")
    search_fields = ("blog__title", "og_title", "og_description")
    ordering = ("-created_at",)
    list_filter = ("blog__category",)
    list_per_page = 20
    date_hierarchy = "created_at"


@admin.register(SeoTwitterBlogData)
class SeoTwitterBlogDataAdmin(ModelAdmin, TabbedTranslationAdmin):
    """
    Admin interface for SeoTwitterBlogData model.
    """

    list_display = ("blog", "twitter_title", "twitter_description", "twitter_image")
    search_fields = ("blog__title", "twitter_title", "twitter_description")
    ordering = ("-created_at",)
    list_filter = ("blog__category",)
    list_per_page = 20
    date_hierarchy = "created_at"
