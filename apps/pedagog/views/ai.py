from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.choices.role import Role
from apps.pedagog.models.ai import Ai, AiType
from apps.pedagog.serializers.ai import AiSerializer


class AiAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        type = request.query_params.get("type", None)
        topic = request.query_params.get("id", None)
        queryset = Ai.objects.all()

        if type == AiType.ALL:
            queryset = queryset.filter(type=AiType.ALL)
        elif type == AiType.TOPIC:
            if topic is not None:
                queryset = queryset.filter(topic=topic)
            else:
                return Response(
                    {"detail": _("Topic ID is required for type 'TOPIC'.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"detail": _("Invalid type parameter.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AiSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.role == Role.MODERATOR or request.user.role == Role.ADMIN:
            raise PermissionDenied(_("Sizda buni amalga oshirishga ruxsat yo'q."))

        data = request.data
        for item in data:
            if item.get("type") == AiType.TOPIC and not item.get("topic"):
                return Response(
                    {"detail": _("Topic ID is required for type 'TOPIC'.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if item.get("type") == AiType.ALL and item.get("topic"):
                return Response(
                    {"detail": _("Topic ID should not be present for type 'ALL'.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            item_serializer = AiSerializer(data=item, context={"request": request})
            item_serializer.is_valid(raise_exception=True)
            item_serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data={"detail": _("Success")})


def patch(self, request, *args, **kwargs):
    instance_id = request.query_params.get("id")
    if not instance_id:
        return Response(
            {"detail": _("ID is required.")},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        instance = Ai.objects.get(id=instance_id)
    except Ai.DoesNotExist:
        return Response(
            {"detail": _("Instance not found.")},
            status=status.HTTP_404_NOT_FOUND,
        )

    if instance.user != request.user:
        raise PermissionDenied(_("Sizda buni amalga oshirishga ruxsat yo'q."))

    serializer = AiSerializer(
        instance,
        data=request.data,
        partial=True,
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
