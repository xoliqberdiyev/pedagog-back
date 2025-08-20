from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pedagog.filters.plan import MediaFilter
from apps.pedagog.models.media import Media
from apps.pedagog.models.moderator import Moderator
from apps.pedagog.models.plan import Plan
from apps.pedagog.permissions.plan import PlanPermission
from apps.pedagog.serializers.plan import (
    PlanSerializer,
    PlanDetailSerializer,
    PlanAdminListSerializer,
)
from apps.shared.pagination.custom import CustomPagination


class PlanApiView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def post(self, request):
        self.permission_classes = [
            AllowAny,
            PlanPermission(["moderator"]),
        ]
        plan_serializer = PlanSerializer(
            data=request.data, context={"request": request}
        )
        plan_serializer.is_valid(raise_exception=True)
        plan_serializer.save()
        return Response(plan_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        school_type = request.query_params.get("school_type", None)
        classes = request.query_params.get("classes", None)
        science = request.query_params.get("science", None)
        science_language = request.query_params.get("science_language", None)
        quarter = request.query_params.get("quarter", None)

        if Moderator.objects.filter(user=user).exists():
            moderator = Moderator.objects.get(user=user)
            plans = Plan.objects.filter(
                school_type__in=moderator.school_type.all(),
                classes__in=moderator.classes.all(),
                science__in=moderator.science.all(),
                science_language__in=moderator.science_language.all(),
                quarter__in=moderator.quarters.all(),
            )
        else:
            plans = Plan.objects.filter(is_active=True)

        if school_type:
            plans = plans.filter(school_type=school_type)
        if classes:
            plans = plans.filter(classes=classes)
        if science:
            plans = plans.filter(science=science)
        if science_language:
            plans = plans.filter(science_language=science_language)
        if quarter:
            plans = plans.filter(quarter=quarter)

        paginator = self.pagination_class()
        paginated_plans = paginator.paginate_queryset(plans, request)
        plan_serializer = PlanDetailSerializer(paginated_plans, many=True)
        return paginator.get_paginated_response(plan_serializer.data)


class PlanDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        plan_serializer = PlanDetailSerializer(plan)
        return Response(plan_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk, user=request.user)
        plan_serializer = PlanSerializer(plan, data=request.data, partial=True)
        plan_serializer.is_valid(raise_exception=True)
        plan_serializer.save()
        return Response(plan_serializer.data, status=status.HTTP_200_OK)


class PlanAdminListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Media.objects.all()
    serializer_class = PlanAdminListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MediaFilter

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())

        # Hisob-kitoblar
        user_count = queryset.values("user").distinct().count()
        count = queryset.count()
        total_count = count * 11  # Bu yerda haqiqiy formulani siz belgilang

        response.data.update(
            {
                "user_count": user_count,
                "quarter_count": count,
                "science_count": count,
                "science_type_count": count,
                "science_group_count": count,
                "class_group_count": count,
                "plan_count": count,
                "resource_count": count,
                "resource_type_count": count,
                "media_type_count": count,
                "media_size_count": count,
                "media_create_count": count,
                "total_count": total_count,
            }
        )
        return response
