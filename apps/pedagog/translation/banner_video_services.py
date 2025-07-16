from modeltranslation.translator import TranslationOptions, register

from apps.pedagog.models.banner import BannerModel
from apps.pedagog.models.services import ServicesModel
from apps.pedagog.models.video import VideoModel


@register(BannerModel)
class BannerTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(ServicesModel)
class ServicesTranslationOptions(TranslationOptions):
    fields = ("title", "desc")


@register(VideoModel)
class VideoTranslationOptions(TranslationOptions):
    fields = ("title", "desc")
