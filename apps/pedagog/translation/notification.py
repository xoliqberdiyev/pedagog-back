from modeltranslation.translator import TranslationOptions, register

from apps.websocket.models.notification import Notification


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ("message",)
