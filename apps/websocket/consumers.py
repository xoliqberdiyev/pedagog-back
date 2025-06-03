import asyncio
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.shared.utils.logger import logger
from apps.websocket.models.notification import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def acknowledge_notification(self, notification_id: int) -> None:
        logger.debug(
            f"Attempting to acknowledge notification {notification_id} for user {self.user.id}"
        )
        notification = await Notification.objects.aget(
            id=notification_id, user=self.user
        )
        logger.debug(f"Notification {notification_id} found for user {self.user.id}")
        notification.is_read = True
        await notification.asave()

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                f"user_{self.user.id}", self.channel_name
            )
            await self.accept()

            self.periodic_task = asyncio.create_task(
                self.check_notifications_periodically()
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user_{self.user.id}", self.channel_name
        )
        self.periodic_task.cancel()

    async def check_notifications_periodically(self):
        try:
            while True:
                await self.check_and_send_notifications()
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            pass

    async def check_and_send_notifications(self):
        notifications = await sync_to_async(list)(
            Notification.objects.filter(user=self.user, is_sending=False)  # noqa
        )
        for notification in notifications:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "send_notification",
                        "message": notification.message,
                        "notification_id": notification.id,
                    }
                )
            )
            notification.is_sending = True
            await notification.asave()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data.get("type") == "acknowledge_notification":
            try:
                await self.acknowledge_notification(int(data["notification_id"]))
            except Exception as e:
                logger.error(f"Error acknowledging notification: {e}")

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
