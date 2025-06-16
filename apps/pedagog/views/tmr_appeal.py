from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pedagog.models.tmr_appeal import TMRAppeal, TMRAppealStatus, TmrFiles
from apps.pedagog.serializers.tmr_appeal import TMRAppealSerializer, TmrFilesSerializer
from apps.shared.pagination.custom import CustomPagination
from apps.users.choices.role import Role


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.role == Role.MODERATOR
            or request.user.role == Role.ADMIN
        )


class TMRAppealAPIView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]
    serializer_class = TMRAppealSerializer
    pagination_class = CustomPagination

    def get(self, request):
        user = request.user
        id = request.query_params.get("id")
        queryset = TMRAppeal.objects.filter(user=user)
        status = request.query_params.get("status")
        science = request.query_params.get("science")
        science_language = request.query_params.get("science_language")
        classes = request.query_params.get("classes")
        school_type = request.query_params.get("school_type")

        if id or status or science or science_language or classes or school_type:
            filters = Q()
            if id:
                filters &= Q(id=id)
            if status:
                filters &= Q(status=status)
            if science:
                filters &= Q(science=science)
            if science_language:
                filters &= Q(science_language=science_language)
            if classes:
                filters &= Q(classes=classes)
            if school_type:
                filters &= Q(school_type=school_type)
            queryset = queryset.filter(filters)

        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = TMRAppealSerializer(
                page, many=True, context={"request": request}
            )
            return paginator.get_paginated_response(serializer.data)
        serializer = TMRAppealSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TMRAppealSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TmrFilesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsModerator]
    serializer_class = TmrFilesSerializer

    def post(self, request, *args, **kwargs):
        tmr_id = request.data.get("tmr_appeal")
        if not tmr_id:
            return Response(
                {"tmr_id": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            tmr_appeal = TMRAppeal.objects.get(id=tmr_id)
        except TmrFiles.DoesNotExist:
            return Response(
                {"tmr_id": ["Tmr appeal not found."]},
                status=status.HTTP_404_NOT_FOUND,
            )

        if tmr_appeal.status != TMRAppealStatus.ACCEPTED:
            return Response(
                {"detail": "Tmr appeal status must be accepted to post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TmrFilesSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
