from django.shortcuts import get_object_or_404

from celery import shared_task

from apps.pedagog.utils.preview import create_preview
from apps.pedagog.models.media import Media
from apps.pedagog.models.electron_resource import ElectronResource


@shared_task
def save_preview(media_id):
    media = get_object_or_404(Media, id=media_id)
    file_path = media.file.path
    preview = create_preview(file_path, file_folder='media')
    media.preview = preview
    media.save()
    return f"Media preview saved: {preview}"


@shared_task
def save_preview_for_electron_rosurce(media_id):
    media = get_object_or_404(ElectronResource, id=media_id)
    file_path = media.file.path
    preview = create_preview(file_path, file_folder='electron_resources')
    media.preview = preview
    media.save()
    return f"Electron resource preview saved: {preview}"