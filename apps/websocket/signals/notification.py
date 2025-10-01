from firebase_admin import messaging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.websocket.models.notification import Notification, FSMToken


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    token = FSMToken.objects.filter(user=instance.user).first()
    if token:
        message = messaging.Message(
            notification=messaging.Notification(
                title=instance.title,
                body=instance.body,
                image=instance.image.url if instance.image else None
            ),
            token=token,
        )
        return messaging.send(message)