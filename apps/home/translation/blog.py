from modeltranslation.translator import TranslationOptions, register

from apps.home.models.blog import (
    Blog,
    BlogCategory,
    SeoMetaBlogData,
    SeoOgBlogData,
    SeoTwitterBlogData,
)


@register(BlogCategory)
class BlogCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ("title", "content", "short_title")


@register(SeoMetaBlogData)
class SeoMetaBlogDataTranslationOptions(TranslationOptions):
    fields = ("title", "description", "keywords")


@register(SeoOgBlogData)
class SeoOgBlogDataTranslationOptions(TranslationOptions):
    fields = ("og_title", "og_description")


@register(SeoTwitterBlogData)
class SeoTwitterBlogDataTranslationOptions(TranslationOptions):
    fields = ("twitter_title", "twitter_description", "twitter_card")
