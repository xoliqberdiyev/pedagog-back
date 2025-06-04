from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver

from apps.pedagog.models.moderator import Moderator
from apps.pedagog.models.topic import Topic
from apps.users.choices.role import Role
from apps.users.models.user import User, ContractStatus
from apps.websocket.models.notification import Notification


@receiver(pre_delete, sender=Topic)
def reorder_topics_on_delete(sender, instance, **kwargs):
    related_topics = list(
        Topic.objects.filter(plan_id=instance.plan_id)
        .exclude(id=instance.id)
        .order_by("sequence_number")
    )
    for index, topic in enumerate(related_topics, start=1):
        topic.sequence_number = index
    Topic.objects.bulk_update(related_topics, ["sequence_number"])


@receiver(post_save, sender=Topic)
def reorder_topics_on_save(sender, instance, created, **kwargs):
    related_topics = list(
        Topic.objects.filter(plan_id=instance.plan_id).order_by("sequence_number")
    )
    for index, topic in enumerate(related_topics, start=1):
        topic.sequence_number = index
    Topic.objects.bulk_update(related_topics, ["sequence_number"])


@receiver(m2m_changed, sender=User.document.through)  # M2M relationship changes
def file_status_m2m(sender, instance, action, **kwargs):
    if action == "post_add":  # Trigger after documents are added
        if (
            instance.document.exists()
            and instance.status_file == ContractStatus.NO_FILE
            or instance.status_file == ContractStatus.REJECTED
        ):
            instance.status_file = ContractStatus.WAITING
            instance.save()
            Notification.objects.create(
                user=instance,
                message_uz="Sizning hujjatingiz qabul qilindi",
                message_ru="Ваш документ принят",
            )


@receiver(post_save, sender=User)
def file_status_pre_save(sender, instance, **kwargs):
    if (
        instance.response_file
        and instance.status_file == ContractStatus.WAITING
        and instance.status is False
        and instance.role == Role.MODERATOR
    ):
        User.objects.filter(pk=instance.pk).update(
            status_file=ContractStatus.ACCEPTED, status=True
        )
        if Moderator.objects.filter(user=instance).exists():
            Moderator.objects.filter(user=instance).update(status=True)
        Notification.objects.create(
            user=instance,
            message_uz="Shartnoma qabul qilindi",
            message_ru="Договор принят",
        )
