from django.urls import re_path, path

from apps.websocket.chatconsumer import ChatConsumer
from apps.websocket.consumers import NotificationConsumer
from apps.websocket.views.chat import (
    ChatRoomList,
    MessageList,
    ModeratorMessageUpdate,
    CreateChatRoomApiViews,
)
from apps.websocket.views.notification import NotificationApiView, NotificationDetailApiView

urlpatterns = [
    path("chat/rooms/", ChatRoomList.as_view(), name="chat"),
    path("notification/", NotificationApiView.as_view(), name="notification"),
    path("notification/<int:pk>/", NotificationDetailApiView.as_view(), name="notification-detail"),
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
