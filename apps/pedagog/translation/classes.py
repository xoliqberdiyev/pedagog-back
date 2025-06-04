from modeltranslation.translator import TranslationOptions, register

from apps.pedagog.models.classes import Classes, ClassGroup


@register(Classes)
class ClassesTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(ClassGroup)
class ClassGroupTranslationOptions(TranslationOptions):
    fields = ("name",)
