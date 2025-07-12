from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.moderator.models.permission import (
    ModeratorPermission,
    ModeratorPermissionStatus,
)
from apps.pedagog.models.moderator import Moderator
from apps.shared.utils.logger import logger
from apps.shared.utils.sms import send_message


@receiver(post_save, sender=ModeratorPermission)
def update_permission_cache(sender, instance, created, **kwargs):
    user = instance.user
    moderator = Moderator.objects.filter(user=user).first()
    if (
        instance._status != ModeratorPermissionStatus.APPROVED.value
        and instance.status == ModeratorPermissionStatus.APPROVED.value
    ):
        send_message(
            user.phone,
            "{first_name} {last_name} sizning {classroom} {science} fanidan pedagog.uz da resurslarni yuklash uchun topshirgan arizangiz tasdiqlandi!".format(
                first_name=user.first_name,
                last_name=user.last_name,
                classroom=instance.classes.first().name,
                science=instance.science.first().name,
            ),
        )
    if moderator:
        if hasattr(instance, "science"):
            for sci in instance.science.all():
                if not moderator.science.filter(pk=sci.pk).exists():
                    moderator.science.add(sci)
        if hasattr(instance, "science_language"):
            for sl in instance.science_language.all():
                if not moderator.science_language.filter(pk=sl.pk).exists():
                    moderator.science_language.add(sl)
        if hasattr(instance, "classes"):
            for cl in instance.classes.all():
                if not moderator.classes.filter(pk=cl.pk).exists():
                    moderator.classes.add(cl)
        if hasattr(instance, "school_type"):
            for st in instance.school_type.all():
                if not moderator.school_type.filter(pk=st.pk).exists():
                    moderator.school_type.add(st)
        logger.info(f"Updated permissions cache for moderator: {moderator.user.phone}")
    else:
        logger.info(f"No moderator found for user: {instance.user.username}")
