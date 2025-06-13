from modeltranslation.translator import TranslationOptions, register

from apps.pedagog.models.degree import Degree


@register(Degree)
class DegreeTranslationOptions(TranslationOptions):
    fields = ("name",)
