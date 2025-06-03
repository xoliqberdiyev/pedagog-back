from modeltranslation.translator import TranslationOptions, register

from apps.pedagog.models.science import Science, ScienceLanguage


@register(Science)
class ScienceTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(ScienceLanguage)
class ScienceLanguageTranslationOptions(TranslationOptions):
    fields = ("name",)
