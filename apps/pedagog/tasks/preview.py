from django.shortcuts import get_object_or_404

from celery import shared_task

from apps.pedagog.utils.preview import create_preview
from apps.pedagog.models.media import Media


@shared_task
def save_preview(media_id):
    media = get_object_or_404(Media, id=media_id)
    file_path = media.file.path
    preview = create_preview(file_path)
    media.preview = preview
    media.save()
    return f"Media preview saved: {preview}"