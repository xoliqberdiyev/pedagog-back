from modeltranslation.translator import TranslationOptions, register

from apps.pedagog.models.classes import Classes


@register(Classes)
class ClassesTranslationOptions(TranslationOptions):
    fields = ("name",)
