from modeltranslation.translator import TranslationOptions, register

from apps.pedagog.models.electron_resource import (
    ElectronResourceCategory,
    ElectronResourceSubCategory,
    SeoMetaCategoryData,
    SeoOgCategoryData,
    SeoTwitterCategoryData,
)


@register(ElectronResourceCategory)
class ElectronResourceCategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(ElectronResourceSubCategory)
class ElectronResourceSubCategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(SeoMetaCategoryData)
class SeoMetaCategoryDataTranslationOptions(TranslationOptions):
    fields = ("title", "description", "keywords")


@register(SeoOgCategoryData)
class SeoOgCategoryDataTranslationOptions(TranslationOptions):
    fields = ("og_title", "og_description")


@register(SeoTwitterCategoryData)
class SeoTwitterCategoryDataTranslationOptions(TranslationOptions):
    fields = ("twitter_title", "twitter_description", "twitter_card")
