from modeltranslation.translator import TranslationOptions, register

from apps.users.models.locations import Region, District


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ("name",)
