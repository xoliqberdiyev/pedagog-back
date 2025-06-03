from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.websocket.models.chat import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    autocomplete_fields = ("participants", "last_message")
    search_fields = ("participants__phone",)


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ("id", "chat", "sender", "message", "created_at")
    search_fields = ("chat__participants__username", "sender__username")
    autocomplete_fields = ("chat", "sender")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("chat", "sender")
