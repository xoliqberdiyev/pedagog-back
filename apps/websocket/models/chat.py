from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class ChatRoom(AbstractBaseModel):
    """
    Chat xonasi modeli. Har bir user va adminlar o'rtasida alohida chat xonasi bo'ladi.
    """

    name = models.CharField(
        max_length=255, blank=True, null=True, help_text="Chat nomi."
    )
    participants = models.ManyToManyField("users.User", related_name="chats")
    message_count = models.PositiveBigIntegerField(
        default=0, help_text="O'qilmagan xabarlar soni."
    )
    last_message = models.ForeignKey(
        "Message",
        on_delete=models.SET_NULL,
        related_name="last_message",
        null=True,
        blank=True,
        help_text="Chatdagi oxirgi xabar.",
    )

    def __str__(self):
        return f"Chat {self.id} - {', '.join([user.username for user in self.participants.all()])}"

    class Meta:
        verbose_name = _("Chat Room")
        verbose_name_plural = _("Chat Rooms")
        ordering = ["-created_at"]
        db_table = "chat_rooms"


class Message(AbstractBaseModel):
    """
    Xabarlar modeli. Chatda yozilgan xabarlarni saqlash uchun ishlatiladi.
    """

    chat = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages",
        help_text="Xabar tegishli bo'lgan chat xonasi.",
    )
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        help_text="Xabarni yuborgan foydalanuvchi.",
        related_name="sent_messages",
    )
    message = models.TextField(blank=True, null=True, help_text="Xabar matni.")
    file = models.FileField(
        upload_to="chat_files/",
        blank=True,
        null=True,
        help_text="Xabar fayli.",
    )
    is_read = models.BooleanField(
        default=False, help_text="Xabar o'qilganligini bildiradi."
    )

    def __str__(self):
        return f"Message {self.id} - {self.sender.username}"

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ["created_at"]
        db_table = "messages"
