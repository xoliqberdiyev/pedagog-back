from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.moderator.models.permission import ModeratorPermission
from apps.pedagog.models.moderator import Moderator
from apps.shared.utils.logger import logger


@receiver(post_save, sender=ModeratorPermission)
def update_permission_cache(sender, instance, created, **kwargs):
    moderator = Moderator.objects.filter(user=instance.user).first()
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
