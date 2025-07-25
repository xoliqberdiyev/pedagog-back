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


def convert_pptx_to_images(pptx_path, output_dir, max_pages=6):
    # 1. PDFga aylantiramiz
    pdf_path = os.path.splitext(pptx_path)[0] + ".pdf"
    try:
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", os.path.dirname(pptx_path),
            pptx_path
        ], check=True)
    except subprocess.CalledProcessError:
        raise Exception("LibreOffice bilan .pptx faylni PDFga aylantirib bo‘lmadi.")

    # 2. PDFni rasmga aylantiramiz
    image_paths = convert_pdf_to_images(pdf_path, output_dir, max_pages)

    # 3. Vaqtincha pdf faylni o‘chirish (ixtiyoriy)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

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

def add_multiple_icons_to_image(image_path, icon_path, positions=None, opacity=128, scale=0.2):
    if positions is None:
        positions = ['top-left', 'center', 'bottom-right']

    base_image = Image.open(image_path).convert("RGBA")
    icon_original = Image.open(icon_path).convert("RGBA")

    # Iconni masshtablash
    icon_width = int(base_image.width * scale)
    icon_ratio = icon_width / icon_original.width
    icon_height = int(icon_original.height * icon_ratio)
    icon_resized = icon_original.resize((icon_width, icon_height), Image.FIXED)

    if opacity < 255:
        alpha = icon_resized.split()[3]
        alpha = alpha.point(lambda p: p * (opacity / 255))
        icon_resized.putalpha(alpha)

    for pos in positions:
        if pos == 'top-left':
            x, y = 10, 10
        elif pos == 'center':
            x = (base_image.width - icon_resized.width) // 2
            y = (base_image.height - icon_resized.height) // 2
        elif pos == 'bottom-right':
            x = base_image.width - icon_resized.width - 10
            y = base_image.height - icon_resized.height - 10
        else:
            continue

        base_image.paste(icon_resized, (x, y), icon_resized)

    base_image = base_image.convert("RGB")
    base_image.save(image_path)


def convert_office_to_pdf(file_path, output_dir):
    pdf_path = os.path.splitext(file_path)[0] + ".pdf"
    try:
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            file_path
        ], check=True)
    except subprocess.CalledProcessError:
        raise Exception("LibreOffice orqali faylni PDFga aylantirishda xatolik.")
    return os.path.join(output_dir, os.path.basename(pdf_path))


def convert_office_file_to_images(file_path, output_dir, max_pages=6):
    ext = os.path.splitext(file_path)[1].lower()
    supported = ['.ppt', '.pptx', '.doc', '.docx']
    if ext not in supported:
        raise ValueError("Fayl turi qo‘llab-quvvatlanmaydi: " + ext)

    pdf_path = convert_office_to_pdf(file_path, output_dir)

    images = convert_pdf_to_images(pdf_path, output_dir, max_pages=max_pages)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    return images