from django.urls import re_path, path, include
from rest_framework.routers import DefaultRouter

from apps.websocket.chatconsumer import ChatConsumer
from apps.websocket.consumers import NotificationConsumer
from apps.websocket.views.chat import (
    ChatRoomList,
    MessageList,
    ModeratorMessageUpdate,
    CreateChatRoomApiViews,
)
from apps.websocket.views.notification import NotificationViewSet

router = DefaultRouter()
router.register("notification", NotificationViewSet, basename="notification")

urlpatterns = [
    path("", include(router.urls)),
    path("chat/rooms/", ChatRoomList.as_view(), name="chat"),
    path("message/", MessageList.as_view(), name="message"),
    path("message/<int:pk>/", MessageList.as_view(), name="message"),
    path(
        "message/<int:pk>/",
        ModeratorMessageUpdate.as_view(),
        name="message-update",
    ),
    path(
        "create/chat/rooms/",
        CreateChatRoomApiViews.as_view(),
        name="create-chat-room",
    ),
]

websocket_urlpatterns = [
    re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
    re_path(r"ws/chat/$", ChatConsumer.as_asgi()),
]
