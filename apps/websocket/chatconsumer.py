import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework_simplejwt.tokens import AccessToken

from apps.shared.utils.logger import logger
from apps.websocket.models.chat import ChatRoom

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_params = self.scope["query_string"].decode()
        token = self._get_token_from_query(query_params)
        self.scope["user"] = await self._get_user_from_token(token)

        if self.scope["user"] and self.scope["user"].is_authenticated:
            cache.set(
                f"channel_{self.scope['user'].username}",
                self.channel_name,
                60 * 60 * 24,
            )

        user_groups = await self._get_user_groups()
        print(f"User groups: {user_groups}")
        await self._add_groups(user_groups)
        await self.accept()

    async def disconnect(self, close_code):
        """
        Guruhlardan uzilish.
        """
        user_groups = await self._get_user_groups()
        await self._remove_groups(user_groups)

    async def receive(self, text_data):
        if not self.scope["user"] or self.scope["user"].is_anonymous:
            return await self.send(
                text_data=json.dumps({"status": False, "detail": "Unauthorized"})
            )
        await self.send(json.dumps({"success": True, "data": None}))

    async def chat_message(self, event):
        """
        Chatga yuboriladigan xabarlar uchun handler.
        """
        # event nusxasini olish kerak chunki event barcha foydalanuvchilar uchun umumiy
        data = event.copy()
        data.pop("type", None)
        await self.send(
            text_data=json.dumps(
                {
                    "status": True,
                    "data": data,
                }
            )
        )

    def _get_data(self, text_data) -> dict:
        """
        Kiruvchi JSON ma'lumotlarini pars qilish.
        """
        try:
            return json.loads(text_data)
        except json.JSONDecodeError:
            return {}

    async def _add_groups(self, chats):
        for chat in chats:
            logger.info(chat)
            await self.channel_layer.group_add(chat, self.channel_name)

    async def _remove_groups(self, chats):
        """
        Foydalanuvchini guruhlardan chiqarish.
        """
        for chat in chats:
            await self.channel_layer.group_discard(chat, self.channel_name)

    @sync_to_async
    def _get_user_groups(self) -> list:
        """
        Foydalanuvchi ishtirok etayotgan chat guruhlarini olish.
        """
        user = self.scope.get("user")
        if user and user.is_authenticated:
            chat = ChatRoom.objects.values_list("id", flat=True)
            return [f"chat_{chat_id}" for chat_id in chat]
        return []

    def _get_token_from_query(self, query_params):
        """
        Query string ichidan tokenni olish.
        """
        params = dict(x.split("=") for x in query_params.split("&") if "=" in x)
        return params.get("token")

    @sync_to_async
    def _get_user_from_token(self, token):
        """
        Token orqali foydalanuvchini olish.
        """
        if not token:
            return None
        try:
            access_token = AccessToken(token)
            return User.objects.get(id=access_token["user_id"])
        except (User.DoesNotExist, Exception):
            return None
