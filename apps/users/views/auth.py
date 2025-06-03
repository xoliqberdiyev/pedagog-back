from typing import Type

from django.utils import translation
from rest_framework import permissions, request, throttling
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.shared.enums import Messages
from apps.shared.services.sms import SmsService
from apps.users.serializers.auth import ResendSerializer


class AbstractSendSms(APIView):
    serializer_class = ResendSerializer
    throttle_classes = [throttling.UserRateThrottle]
    permission_classes = [permissions.AllowAny]

    def post(self, rq: Type[request.Request]):
        language = rq.headers.get("Accept-Language", "uz")
        sms_service = SmsService()
        translation.activate(language)
        ser = self.serializer_class(data=rq.data)
        ser.is_valid(raise_exception=True)
        phone = ser.data.get("phone")
        sms_service.send_confirm(phone, language)
        return Response(
            {"success": True, "message": Messages.SEND_MESSAGE},
            status=200,
        )
