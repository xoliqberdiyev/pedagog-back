import datetime
import os
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.models.models import Orders
from apps.pedagog.models.download import Download
from apps.pedagog.models.download_token import DownloadToken
from apps.pedagog.models.media import Media
from apps.pedagog.serializers.download_history import (
    DownloadHistorySerializer,
    UploadMediaSerializer,
)
from apps.shared.pagination.custom import CustomPagination
from apps.users.choices.role import Role


class DownloadMediaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, media_id, format=None):
        user = request.user
        current_date = datetime.date.today()
        media = get_object_or_404(Media, id=media_id)

        # Check if media has an associated topic
        topic = media.topic_id
        plan = topic.plan_id if topic else None

        order = None
        if plan:
            order = Orders.objects.filter(
                user=user,
                classes=plan.classes,
                science=plan.science,
                science_language=plan.science_language,
                start_date__lte=current_date,
                end_date__gte=current_date,
                status=True,
            ).last()

        # If media has a topic, only the owner or a user with an order can download
        if (plan and media.user != user and user.role == Role.MODERATOR
                or user.role == Role.ADMIN):
            raise Http404(_("Ushbu resurslar sizga tegishli emas"))

        if plan and not order and user.role == Role.USER:
            raise Http404(
                _("Bu resursni yuklab olish uchun buyurtma berishingiz kerak"))

        download = Download.objects.create(
            user=user,
            media=media,
            date=current_date,
            object_type="plan",
            object_id=topic.id,
        )

        if plan:
            if user.role != Role.MODERATOR or user.role != Role.ADMIN:
                if not download.media.download_users.filter(
                        id=user.id).exists():
                    download.media.download_users.add(user)
                    download.media.count += 1
                    download.media.save()
        else:
            if not download.media.download_users.filter(id=user.id).exists():
                download.media.download_users.add(user)
                download.media.count += 1
                download.media.save()

        science = plan.science if plan else None
        users_count = ((Orders.objects.filter(
            science=science).values("user").distinct().count())
                       if science else 0)

        users_count = min(users_count, 1)
        download_users_count = download.media.download_users.count()

        download.media.statistics = ((
            f"{(users_count / download_users_count) * 100}%")
                                     if download_users_count > 0 else "0%")
        download.media.save()

        download_token = DownloadToken.objects.create(
            download=download,
            expires_at=timezone.now() + datetime.timedelta(minutes=5),
        )

        download_url = download_token.token

        return Response({"download_token": download_url})


class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, download_token, format=None):
        download_token = get_object_or_404(DownloadToken, token=download_token)

        if download_token.is_expired():
            raise Http404(
                _("Yuklab olish tokeni topilmadi yoki muddati oʻtgan"))

        download = download_token.download

        media = get_object_or_404(Media, id=download.media.id)

        file_path = media.file.path

        try:
            filename = os.path.basename(media.file.name)
            response = FileResponse(open(file_path, "rb"),
                                    as_attachment=True,
                                    filename=smart_str(filename))
        except FileNotFoundError:
            raise Http404(_("Fayl topilmadi"))

        download_token.delete()

        return response


############################################################################################################
# Yuklab olingan resurs media fayllarini ro'yxatini olish mobile uchun
############################################################################################################
@extend_schema(parameters=[
    OpenApiParameter(
        name="type",
        description="Type of download (required)",
        required=True,
        type=str,
    ),
    OpenApiParameter(
        name="topic_name",
        description="Filter by topic name (only for type 'plan')",
        required=False,
        type=str,
    ),
    OpenApiParameter(
        name="time_range",
        description="Filter by time range (e.g., last_hour, last_2_hours, "
        "last_3_hours, last_24_hours, last_4_weeks)",
        required=False,
        type=str,
    ),
])
class MobileDownloadHistoryView(generics.ListAPIView):
    serializer_class = DownloadHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Download.objects.filter(user=user)
        topic_name = self.request.query_params.get("topic_name")
        time_range = self.request.query_params.get("time_range")

        if topic_name:
            try:
                queryset.filter(media__topic_id__name__icontains=topic_name)
            except ObjectDoesNotExist:
                queryset = queryset.none()

        if time_range:
            now = timezone.now()
            if time_range == "last_hour":
                queryset = queryset.filter(created_at__gte=now -
                                           timedelta(hours=1))
            elif time_range == "last_2_hours":
                queryset = queryset.filter(created_at__gte=now -
                                           timedelta(hours=2))
            elif time_range == "last_3_hours":
                queryset = queryset.filter(created_at__gte=now -
                                           timedelta(hours=3))
            elif time_range == "last_24_hours":
                queryset = queryset.filter(created_at__gte=now -
                                           timedelta(hours=24))
            elif time_range == "last_4_weeks":
                queryset = queryset.filter(created_at__gte=now -
                                           timedelta(weeks=4))

        return queryset


############################################################################################################
# Yuklab olingan resurs media fayllarini ro'yxatini olish
############################################################################################################
@extend_schema(parameters=[
    OpenApiParameter(
        name="type",
        description="Type of resource (required, 'resource' or 'plan')",
        required=True,
        type=str,
    ),
    OpenApiParameter(
        name="time_range",
        description=
        "Filter by time range (last_hour, last_2_hours, last_3_hours, last_24_hours, last_4_weeks)",
        required=False,
        type=str,
    ),
    OpenApiParameter(
        name="search",
        description="Search by name",
        required=False,
        type=str,
    ),
])
class MobileUploadHistoryView(generics.ListAPIView):
    serializer_class = UploadMediaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Media.objects.filter(user=user)
        topic_name = self.request.query_params.get("topic_name")
        time_range = self.request.query_params.get("time_range")

        if topic_name:
            try:
                queryset.filter(topic_id__name__icontains=topic_name)
            except ObjectDoesNotExist:
                queryset = queryset.none()

        if time_range:
            now = timezone.now()
            if time_range == "last_hour":
                queryset = queryset.filter(created_at__gte=now -
                                           timedelta(hours=1))
            elif time_range == "last_2_hours":
                queryset = queryset.filter(created_at__gte=now -
                                           timedelta(hours=2))
            elif time_range == "last_3_hours":
                queryset = queryset.filter(created_at__gte=now -
                                           timedelta(hours=3))
            elif time_range == "last_24_hours":
                queryset = queryset.filter(created_at__gte=now -
                                           timedelta(hours=24))
            elif time_range == "last_4_weeks":
                queryset = queryset.filter(created_at__gte=now -
                                           timedelta(weeks=4))

        return queryset
