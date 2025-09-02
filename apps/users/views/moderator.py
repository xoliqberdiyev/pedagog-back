import json
import os

import redis
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from apps.pedagog.models.documents import Document, FileModel
from apps.shared.services.sms import SmsService
from apps.users.serializers.auth import ModeratorRegisterSerializer

from apps.users.models.user import SourceChoice

redis_instance = redis.StrictRedis.from_url(os.getenv("REDIS_CACHE_URL"))


class ModeratorRegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]
    serializer_class = ModeratorRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]

            # Fayllarni olish
            docs = serializer.validated_data.get("docs", [])
            docs_id = []

            for file_obj in docs:
                # Faylni saqlash
                document = Document.objects.create()
                document.document_file.add(FileModel.objects.create(file=file_obj))
                docs_id.append(document.id)

            # Fayl IDlarini JSON shaklida saqlash
            data = {
                k: (
                    json.dumps(v, cls=DjangoJSONEncoder)
                    if isinstance(v, (dict, list, tuple))
                    else str(v)
                )
                for k, v in serializer.validated_data.items()
                if k != "docs"  # `docs`ni alohida qayta ishlaymiz
            }

            # `docs` maydonini saqlash
            data["docs"] = json.dumps(docs_id)
            data["type"] = "moderator"


            header_source = request.headers.get("source", None)
            if header_source in SourceChoice.values:
                source = header_source
            else:
                source = SourceChoice.WEB
            data["type"] = "moderator"
            data["source"] = source


            # Redisda saqlash
            redis_instance.delete(phone)
            redis_instance.hset(phone, mapping=data)

            # Tilni olish
            language = request.headers.get("Accept-Language", "uz")
            sms_service = SmsService()
            sms_service.send_confirm(phone, language)

            return Response(
                {
                    "success": True,
                    "message": _(
                        f"Registration data saved. Please confirm your code. SMS sent to {phone} phone number."
                    ),
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "success": False,
                "message": _("Invalid data."),
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
