import json
import os
import typing
import uuid

import redis
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework import request as rest_request
from rest_framework import response, status, views, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.pedagog.models.degree import Degree
from apps.pedagog.models.documents import Document
from apps.pedagog.models.moderator import Moderator
from apps.shared.enums import Messages
from apps.shared.exceptions.core import SmsException
from apps.shared.services.sms import SmsService
from apps.users.models.locations import Region, District
from apps.users.models.reset_token import ResetToken
from apps.users.models.user import User, BotUsers
from apps.users.serializers.auth import (
    RegisterSerializer,
    ConfirmSerializer,
    ResetConfirmationSerializer,
    ResendSerializer,
    ResetPasswordSerializer,
)
from apps.users.serializers.custom_token import CustomTokenObtainPairSerializer
from apps.users.serializers.set_password import SetPasswordSerializer
from apps.users.serializers.user import (
    UserDetailSerializer,
    UserSerializer,
    UserUpdateSerializer,
    BotUsersSerialiers
)

from apps.users.models.user import SourceChoice
from apps.users.views.auth import AbstractSendSms
from rest_framework.exceptions import ValidationError


redis_instance = redis.StrictRedis.from_url(os.getenv("REDIS_CACHE_URL"))




class BotUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        tg_id = request.data.get('tg_id')

        if BotUsers.objects.filter(tg_id=tg_id).exists():
            return Response(
                {"message": "User with this tg_id already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BotUsersSerialiers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )



class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]

            referral_code = request.headers.get("Referral-Code", None)
            ref_user_id = None
            if referral_code:
                try:
                    ref_user = User.objects.get(referral_code=referral_code)
                    ref_user_id = int(ref_user.id)
                    print(type(ref_user_id))
                except User.DoesNotExist:
                    ref_user_id = None

            data = {
                k: (
                    json.dumps(v, cls=DjangoJSONEncoder)
                    if isinstance(v, (dict, list, tuple))
                    else str(v)
                )
                for k, v in serializer.validated_data.items()
            }

            if ref_user_id:
                data["referred_by"] = int(ref_user_id)

            header_source = request.headers.get("source", None)
            if header_source in SourceChoice.values:
                source = header_source
            else:
                source = SourceChoice.WEB
            data["type"] = "user"
            data["source"] = source

            redis_instance.delete(phone)
            redis_instance.hset(phone, mapping=data)

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
                status=201,
            )

        return Response(
            {
                "success": False,
                "message": _("Invalid data."),
                "data": serializer.errors,
            },
            status=400,
        )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            detail = e.detail
            if isinstance(detail, dict) and "detail" in detail:
                detail = detail["detail"]
            if isinstance(detail, list):
                detail = detail[0]

            return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)



class ConfirmView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            code = serializer.validated_data["code"]
            user = None
            try:
                if SmsService.check_confirm(phone, code=code):
                    user_data = redis_instance.hgetall(phone)
                    if user_data:
                        try:
                            region_instance = Region.objects.filter(
                                id=user_data[b"region"].decode("utf-8")
                            ).first()
                            if not region_instance:
                                return Response(
                                    {
                                        "success": False,
                                        "message": _("Region not found."),
                                    },
                                    status=status.HTTP_400_BAD_REQUEST,
                                )
                            district_instance = District.objects.filter(
                                id=user_data[b"district"].decode("utf-8")
                            ).first()
                            if not district_instance:
                                return Response(
                                    {
                                        "success": False,
                                        "message": _("District not found."),
                                    },
                                    status=status.HTTP_400_BAD_REQUEST,
                                )
                                
                            referred_by_id = user_data.get(b"referred_by")
                            referrer = None
                            if referred_by_id:
                                referrer = User.objects.filter(id=int(referred_by_id)).first()
                                
                            user = User.objects.create_user(
                                phone=phone,
                                first_name=user_data[b"first_name"].decode("utf-8"),
                                last_name=user_data[b"last_name"].decode("utf-8"),
                                father_name=user_data[b"father_name"].decode("utf-8"),
                                region=region_instance,
                                district=district_instance,
                                source=user_data[b"source"].decode("utf-8"),
                                referred_by=referrer,  
                                institution_number=user_data[
                                    b"institution_number"
                                ].decode("utf-8"),
                                password=user_data[b"password"].decode("utf-8"),
                            )
                            if user_data[b"type"].decode("utf-8") == "moderator":
                                degree_instance = Degree.objects.filter(
                                    id=user_data[b"degree"].decode("utf-8")
                                ).first()
                                user.role = "moderator"
                                user.save(update_fields=["role"])
                                moderator, created = Moderator.objects.update_or_create(
                                    user=user,
                                    defaults={"degree": degree_instance},
                                )
                                docs_data = json.loads(
                                    user_data[b"docs"].decode("utf-8")
                                )
                                for doc_data in docs_data:
                                    try:
                                        doc = Document.objects.get(id=doc_data)
                                    except Document.DoesNotExist:
                                        continue
                                    doc.user = user
                                    doc.save(update_fields=["user"])
                                    moderator.docs.add(doc_data)
                            redis_instance.delete(phone)
                        except IntegrityError as e:
                            if "duplicate key value violates unique constraint" in str(
                                e
                            ):
                                return Response(
                                    {
                                        "success": False,
                                        "message": _("Phone number already exists."),
                                    },
                                    status=status.HTTP_400_BAD_REQUEST,
                                )
                            return Response(
                                {"success": False, "message": str(e)},
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    token = user.tokens()
                    return Response(
                        {
                            "success": True,
                            "message": _("User created."),
                            "data": {
                                "access": token["access"],
                                "refresh": token["refresh"],
                            },
                        },
                        status=status.HTTP_201_CREATED,
                    )
            except SmsException as e:
                return Response(
                    {"success": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                return Response(
                    {"success": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"success": False, "message": _("Invalid phone number or code.")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "success": False,
                "message": _("Invalid data."),
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ResetConfirmationCodeView(views.APIView):
    """Reset confirm otp code"""

    serializer_class = ResetConfirmationSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=serializer_class,
        summary="Reset confirm otp code.",
        description="Reset confirm otp code.",
    )
    def post(self, request: rest_request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.data
        code, phone = data.get("code"), data.get("phone")
        try:
            res = SmsService.check_confirm(phone, code)
            if res:
                token = ResetToken.objects.create(
                    user=User.objects.filter(phone=phone).first(),
                    token=str(uuid.uuid4()),
                )
                return response.Response(
                    data={
                        "token": token.token,
                        "created_at": token.created_at,
                        "updated_at": token.updated_at,
                    },
                    status=status.HTTP_200_OK,
                )
            return response.Response(
                data={"detail": _(Messages.INVALID_OTP)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except SmsException as e:
            return response.Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return response.Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)


class ResetSetPasswordView(views.APIView):
    serializer_class = SetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=serializer_class,
        summary="Reset user password.",
        description="Reset user password.",
    )
    def post(self, request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        token = data.get("token")
        password = data.get("password")
        token = ResetToken.objects.filter(token=token)
        if not token.exists():
            return response.Response(
                {"detail": _("Token xato")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        phone = token.first().user.phone
        token.delete()
        user = User.objects.filter(phone=phone).first()
        user.set_password(password)
        user.save()
        return response.Response(
            {"detail": _("Parol yangilandi")}, status=status.HTTP_200_OK
        )


class ResendView(AbstractSendSms):
    """Resend Otp Code"""

    serializer_class = ResendSerializer


class ResetPasswordView(AbstractSendSms):
    """Reset user password"""

    serializer_class: typing.Type[ResetPasswordSerializer] = ResetPasswordSerializer


class MeView(viewsets.ViewSet):
    """Get user information"""

    serializer_class = UserDetailSerializer

    @extend_schema(
        request=serializer_class,
        summary="Get user information.",
        description="Get user information.",
    )
    def get(self, request: rest_request.Request):
        user = request.user
        return response.Response(
            UserDetailSerializer(user, context={"request": request}).data
        )


class MeUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user
