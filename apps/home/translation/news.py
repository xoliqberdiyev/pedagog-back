from modeltranslation.translator import TranslationOptions, register

from apps.home.models.news import (
    News,
    NewsCategory,
    SeoMetaNewsData,
    SeoOgNewsData,
    SeoTwitterNewsData,
)


@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
    """
    Translation options for the NewsCategory model.
    """

    fields = ("name",)


@register(News)
class NewsTranslationOptions(TranslationOptions):
    """
    Translation options for the News model.
    """

    fields = ("title", "content", "short_title")


@register(SeoMetaNewsData)
class SeoMetaNewsDataTranslationOptions(TranslationOptions):
    """
    Translation options for the SeoMetaNewsData model.
    """

    fields = ("title", "description", "keywords")


@register(SeoOgNewsData)
class SeoOgNewsDataTranslationOptions(TranslationOptions):
    """
    Translation options for the SeoOgNewsData model.
    """

    fields = ("og_title", "og_description")


@register(SeoTwitterNewsData)
class SeoTwitterNewsDataTranslationOptions(TranslationOptions):
    """
    Translation options for the SeoTwitterNewsData model.
    """

    fields = ("twitter_title", "twitter_description", "twitter_card")
