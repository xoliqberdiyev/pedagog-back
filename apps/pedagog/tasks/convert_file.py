import os
from django.conf import settings
from django.core.files import File
from django.shortcuts import get_object_or_404

from celery import shared_task

from apps.pedagog.models.media import Media
from apps.pedagog.models.converted_media import ConvertedMedia
from apps.shared.utils.convert_image import convert_pdf_to_images, convert_pptx_to_images, convert_docx_to_images, add_multiple_icons_to_image, convert_office_to_pdf


@shared_task
def convert_image_create(media_id):
    media = get_object_or_404(Media, id=media_id)
    file_path = media.file.path

    output_dir = os.path.join(settings.MEDIA_ROOT, "temp_images")
    os.makedirs(output_dir, exist_ok=True)

    type = media.file.name.split(".")[-1]

    if type == 'pdf':
        image_data = convert_pdf_to_images(file_path, output_dir)
    elif type in ['doc', 'docx']:
        image_data = convert_docx_to_images(file_path, output_dir)
    elif type == 'pptx':
        image_data = convert_pptx_to_images(file_path, output_dir)
    elif type == 'ppt':
        pdf_path = convert_office_to_pdf(file_path, output_dir)
        image_data = convert_pdf_to_images(pdf_path, output_dir)
    else:
        raise ValueError(f"Qo‘llab-quvvatlanmaydigan fayl turi: {type}")
        
    for page_number, img_path in image_data:
            add_multiple_icons_to_image(
                img_path,
                './logo.png',
                positions=['top-left', 'center', 'bottom-right'],
                opacity=100, 
                scale=0.25
            )
            with open(img_path, 'rb') as f:
                ConvertedMedia.objects.create(
                    media=media,
                    page_number=page_number,
                    image=File(f, name=os.path.basename(img_path))
                )