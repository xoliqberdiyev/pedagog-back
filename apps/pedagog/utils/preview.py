import os
import subprocess
from django.conf import settings


def create_preview(file_path: str, duration: int = 15) -> str:
    """
    Fayldan preview (mp3/mp4) yaratadi.
    :param file_path: Asl fayl yo'li
    :param duration: Necha soniya preview olish (default = 15)
    :return: preview fayl yo'li (MEDIA ichida)
    """
    filename, ext = os.path.splitext(os.path.basename(file_path))

    if ext.lower() not in [".mp3", ".mp4"]:
        return None  # boshqa format bo‘lsa hech narsa qilmaymiz

    preview_dir = os.path.join(settings.MEDIA_ROOT, "media")
    os.makedirs(preview_dir, exist_ok=True)

    preview_path = os.path.join(preview_dir, f"{filename}_preview{ext}")

    try:
        if ext.lower() == ".mp4":
            # video preview
            cmd = [
                "ffmpeg", "-y",
                "-i", file_path,
                "-t", str(duration),
                "-vf", "scale=640:-2",
                "-c:v", "libx264", "-preset", "veryfast",
                "-c:a", "aac", "-b:a", "128k",
                "-movflags", "+faststart",
                preview_path
            ]
        elif ext.lower() == ".mp3":
            # audio preview (mp3)
            cmd = [
                "ffmpeg", "-y",
                "-ss", "0", "-t", str(duration),
                "-i", file_path,
                "-acodec", "libmp3lame", "-b:a", "128k",
                preview_path
            ]

        subprocess.run(cmd, check=True)

        # return preview MEDIA nisbiy yo‘li
        return f"media/{filename}_preview{ext}"

    except subprocess.CalledProcessError as e:
        print("FFMPEG ERROR:", e)
        return None