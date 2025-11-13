from django.db import models
from django.utils import timezone
from datetime import timedelta
from apps.shared.models.base import AbstractBaseModel


class TelegramMessage(AbstractBaseModel):
    chat_id = models.BigIntegerField(verbose_name="Telegram Chat ID")
    message_id = models.BigIntegerField(verbose_name="Telegram Message ID")
    media = models.ForeignKey("pedagog.Media", on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now, verbose_name="Yuborilgan vaqti")
    deleted = models.BooleanField(default=False)
    


    def is_expired(self):
        return timezone.now() >= self.sent_at + timedelta(days=30)

    def __str__(self):
        return f"Chat {self.chat_id} - Message {self.message_id}"
