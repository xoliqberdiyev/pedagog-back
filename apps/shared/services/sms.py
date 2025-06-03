from datetime import timedelta

from django.utils import timezone
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from apps.shared.exceptions.core import SmsException
from apps.users.models.user import SmsConfirm


class SmsService:
    @staticmethod
    def send_confirm(phone, language):
        translation.activate(language)
        if phone == "946593659":
            code = 1111
        else:
            # TODO: Deploy this change when deploying -> code = random.randint(1000, 9999) # noqa
            # code = random.randint(1000, 9999)
            code = 1111
        sms_confirm, status = SmsConfirm.objects.get_or_create(
            phone=phone, defaults={"code": code}
        )

        sms_confirm.sync_limits()

        if sms_confirm.resend_unlock_time is not None:
            expired = sms_confirm.interval(sms_confirm.resend_unlock_time)
            exception = SmsException(
                _("Qayta yuborish bloklandi, qayta urunib ko'ring {expired}").format(
                    expired=expired
                ),
                expired=expired,
            )
            raise exception

        sms_confirm.code = code
        sms_confirm.try_count = 0
        sms_confirm.resend_count += 1
        sms_confirm.phone = phone
        sms_confirm.expired_time = timezone.now() + timedelta(
            seconds=SmsConfirm.SMS_EXPIRY_SECONDS
        )  # noqa
        sms_confirm.resend_unlock_time = timezone.now() + timedelta(
            seconds=SmsConfirm.SMS_EXPIRY_SECONDS
        )  # noqa
        sms_confirm.save()
        from apps.users.tasks.sms import SendConfirm
        SendConfirm.delay(phone, code, language)
        return True

    @staticmethod
    def check_confirm(phone, code):
        sms_confirm = SmsConfirm.objects.filter(phone=phone).first()

        if sms_confirm is None:
            raise SmsException(_("Invalid confirmation code"))

        sms_confirm.sync_limits()

        if sms_confirm.is_expired():
            raise SmsException(_("Time for confirmation has expired"))

        if sms_confirm.is_block():
            expired = sms_confirm.interval(sms_confirm.unlock_time)
            raise SmsException(_(f"Try again in {expired}"))

        if sms_confirm.code == code:
            sms_confirm.delete()
            return True

        sms_confirm.try_count += 1
        sms_confirm.save()

        raise SmsException(_("Invalid confirmation code"))
