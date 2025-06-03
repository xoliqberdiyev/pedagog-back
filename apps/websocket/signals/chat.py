from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.choices.role import Role
from apps.websocket.models.chat import Message


@receiver(post_save, sender=Message)
def update_chat_room(sender, instance, created, **kwargs):
    """
    Chat xonasi modelini yangilash uchun signal.
    """
    if created:
        instance.chat.message_count = (
            instance.chat.messages.filter(is_read=False, sender__role=Role.USER).count()
            or 0
        )
        instance.chat.last_message = instance
        instance.chat.save()
