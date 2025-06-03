from modeltranslation.translator import TranslationOptions, register

from apps.home.models.seo import Seo


@register(Seo)
class SeoTranslationOptions(TranslationOptions):
    """
    Translation options for the Seo model.
    """

    fields = (
        "title",
        "description",
        "keywords",
        "opengraph_title",
        "opengraph_description",
        "twitter_title",
        "twitter_description",
    )
