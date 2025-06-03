"""
Base celery tasks
"""

from celery import shared_task
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from apps.shared.services.sms_service import SendService
from apps.shared.utils.console import Console


@shared_task
def SendConfirm(phone, code, language):
    translation.activate(language)
    try:
        service: SendService = SendService()
        service.send_sms(
            phone,
            _("pedagog.uz sayti va mobil ilovasi uchun tasdiqlash kodi: %(code)s")
            % {"code": code},
        )
        Console().success(f"Success: {phone}-{code}")
    except Exception as e:
        Console().error(
            "Error: {phone}-{code}\n\n{error}".format(phone=phone, code=code, error=e)
        )  # noqa
