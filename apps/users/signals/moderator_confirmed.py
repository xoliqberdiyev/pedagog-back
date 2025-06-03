from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.users.choices.role import Role
from apps.pedagog.models.moderator import Moderator
from apps.users.models.user import ContractStatus
from apps.users.tasks.moderator_confirmed import send_congratulation_sms
from apps.websocket.models.notification import Notification


@receiver(pre_save, sender=Moderator)
def check_is_contracted_change(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Moderator.objects.get(pk=instance.pk)
        if old_instance.is_contracted and not instance.is_contracted:
            print(f"Old: {old_instance.is_contracted} New: {instance.is_contracted}")
            instance.user.role = Role.USER
            instance.user.status = False
            instance.user.status_file = ContractStatus.REJECTED

            for doc in instance.user.document.all():
                doc.is_active = False
                doc.response_file = instance.user.response_file
                doc.save()
            instance.user.response_file = None
            instance.user.save()
            Notification.objects.create(
                user=instance.user,
                message_uz="Sizning moderatorlik so'rovingiz rad etildi",
                message_ru="Ваш запрос на модераторство был отклонен",
            )
            print("Moderator role changed to user")
        elif not old_instance.is_contracted and instance.is_contracted:
            print(f"Old: {old_instance.is_contracted} New: {instance.is_contracted}")
            first_name = instance.user.first_name
            last_name = instance.user.last_name
            phone = instance.user.phone
            instance.user.role = Role.MODERATOR
            instance.user.save()
            send_congratulation_sms.delay(phone, first_name, last_name)
            print("Moderator confirmed")
