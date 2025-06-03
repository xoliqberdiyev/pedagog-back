from modeltranslation.translator import TranslationOptions, register

from apps.pedagog.models.school import SchoolType


@register(SchoolType)
class SchoolTypeTranslationOptions(TranslationOptions):
    fields = ("name",)
