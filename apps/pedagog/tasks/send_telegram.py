import requests
import os
import time
from apps.pedagog.models.telegram_message import TelegramMessage
from django.utils import timezone
from datetime import timedelta
from celery import shared_task



BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@shared_task
def delete_telegram_message(message_id):
    try:
        message = TelegramMessage.objects.get(id=message_id)
        requests.post(
            f"{TELEGRAM_API}/deleteMessage",
            data={"chat_id": message.chat_id, "message_id": message.message_id}
        )
        message.deleted = True
        message.save()
    except TelegramMessage.DoesNotExist:
        pass
