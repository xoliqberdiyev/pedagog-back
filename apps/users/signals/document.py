from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.pedagog.models.documents import Document
from apps.users.models.user import UserProfile


@receiver(post_save, sender=Document)
def document_save(sender, instance, created, **kwargs):
    if created and instance.user:
        profile, _ = UserProfile.objects.get_or_create(user=instance.user)
        profile.document.add(instance)
