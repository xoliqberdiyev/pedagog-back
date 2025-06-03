from modeltranslation.translator import TranslationOptions, register

from apps.home.models.faq import FAQ


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ("question", "answer")
