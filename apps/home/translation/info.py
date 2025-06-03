from modeltranslation.translator import TranslationOptions, register

from apps.home.models.info import PedagogInfo


@register(PedagogInfo)
class PedagogInfoTranslationOptions(TranslationOptions):
    """
    Translation options for the PedagogInfo model.
    """

    fields = ("title", "description")
