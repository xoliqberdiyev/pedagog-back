"""
Base celery tasks
"""

from celery import shared_task
from django.utils.translation import gettext as _

from apps.shared.services.sms_service import SendService
from apps.shared.utils.console import Console


@shared_task
def send_congratulation_sms(phone, first_name, last_name):
    try:
        service: SendService = SendService()
        service.send_sms(
            phone,
            _(
                "Assalomu alaykum %(first_name)s %(last_name)s sizni https://pedagog.uz o’qituvchining virtual kаbinetida muallif sifatida tasdiqlanganingiz bilan tabriklaymiz!!!"
            )
            % {"first_name": first_name, "last_name": last_name},
        )
        Console().success(f"Success: {phone}-{first_name}-{last_name}")
    except Exception as e:
        Console().error(
            "Error: {phone}-{first_name}-{last_name}\n\n{error}".format(
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                error=e,
            )
        )  # noqa
