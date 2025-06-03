from modeltranslation.translator import TranslationOptions, register

from apps.home.models.privacy import PrivacyPolicy


@register(PrivacyPolicy)
class PrivacyPolicyTranslationOptions(TranslationOptions):
    """
    Translation options for the PrivacyPolicy model.
    """

    fields = ("title", "content")
