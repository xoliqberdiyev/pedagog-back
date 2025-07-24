import io, os, subprocess
from pptx import Presentation
from pdf2image import convert_from_path
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile


def convert_pdf_to_images(pdf_path, output_dir, max_pages=6):
    images = convert_from_path(pdf_path, dpi=200, first_page=1, last_page=max_pages)
    image_paths = []
    for i, img in enumerate(images):
        img_path = f"{output_dir}/page_{i + 1}.png"
        img.save(img_path, "PNG")
        image_paths.append((i + 1, img_path))
    return image_paths


def convert_pptx_to_images(pptx_path, output_dir, max_slides=6):
    prs = Presentation(pptx_path)
    image_paths = []

    for i, slide in enumerate(prs.slides[:max_slides]):
        img = Image.new("RGB", (1280, 720), color=(255, 255, 255))
        img_path = f"{output_dir}/slide_{i + 1}.png"
        img.save(img_path, "PNG")
        image_paths.append((i + 1, img_path))

    return image_paths

def convert_docx_to_images(docx_path, output_dir, max_pages=6):
    pdf_path = os.path.splitext(docx_path)[0] + ".pdf"

    try:
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", os.path.dirname(docx_path),
            docx_path
        ], check=True)
    except subprocess.CalledProcessError:
        raise Exception("LibreOffice orqali DOCXni PDFga o‘zgartirib bo‘lmadi.")

    image_paths = convert_pdf_to_images(pdf_path, output_dir, max_pages=max_pages)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    return image_paths

def add_icon_to_image(image_path, icon_path, position='top-left', opacity=128, scale=0.2):
    base_image = Image.open(image_path).convert("RGBA")
    icon = Image.open(icon_path).convert("RGBA")

    icon_width = int(base_image.width * scale)
    icon_ratio = icon_width / icon.width
    icon_height = int(icon.height * icon_ratio)
    icon = icon.resize((icon_width, icon_height), Image.FIXED)

    if position == 'bottom-right':
        x = base_image.width - icon.width - 10
        y = base_image.height - icon.height - 10
    elif position == 'center':
        x = (base_image.width - icon.width) // 2
        y = (base_image.height - icon.height) // 2
    elif position == 'top-left':
        x, y = 10, 10
    else:
        x, y = 0, 0 

    if opacity < 255:
        alpha = icon.split()[3]
        alpha = alpha.point(lambda p: p * (opacity / 255))
        icon.putalpha(alpha)

    base_image.paste(icon, (x, y), icon)

    base_image = base_image.convert("RGB")
    base_image.save(image_path)