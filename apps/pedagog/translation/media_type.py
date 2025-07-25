from modeltranslation.translator import register, TranslationOptions

from apps.pedagog.models.media_type import MediaType


@register(MediaType)
class MediaTypeTranslation(TranslationOptions):
    fields = ('name',)