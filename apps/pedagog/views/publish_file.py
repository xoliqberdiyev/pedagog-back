import requests
import os
import time as t  # modul time
from django.utils import timezone as django_time
from apps.pedagog.models.telegram_message import TelegramMessage
from apps.pedagog.tasks.send_telegram import delete_telegram_message
from datetime import datetime, time as dtime, timezone 


BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def publish_file(chat_id, file_path, media_instance, delay=0):
    if delay > 0:
        t.sleep(delay)  

    if file_path.startswith("http"):
        file_url = file_path.replace("http://", "https://", 1)
        response = requests.post(
            f"{TELEGRAM_API}/sendDocument",
            data={"chat_id": chat_id, "document": file_url}
        )
    else:
        with open(file_path, "rb") as f:
            response = requests.post(
                f"{TELEGRAM_API}/sendDocument",
                data={"chat_id": chat_id},
                files={"document": f}
            )

    res_json = response.json()
    message_id = res_json["result"]["message_id"]
    print(f"Message ID: {message_id}")

    quarter_end = media_instance.topic_id.plan_id.quarter.end_date

    telegram_message = TelegramMessage.objects.create(
        chat_id=chat_id,
        message_id=message_id,
        media=media_instance,
        sent_at=django_time.now()
    )

    run_time = datetime.combine(quarter_end, dtime(23, 59, 59)).replace(tzinfo=timezone.utc)

    delete_telegram_message.apply_async(
        args=[telegram_message.id],
        eta=run_time
    )

    return message_id
