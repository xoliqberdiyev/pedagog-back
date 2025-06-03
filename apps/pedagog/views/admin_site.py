from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pedagog.choices.degree import Degree
from apps.pedagog.models.moderator import Moderator
from apps.pedagog.serializers.admin_site import ModeratorAdminSiteSerializer
from apps.shared.pagination.custom import CustomPagination


class ModeratorAdminSiteView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ModeratorAdminSiteSerializer

    def get_queryset(self):
        return Moderator.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_contracted",
                description="Is contracted filter",
                required=False,
                type=bool,
            ),
            OpenApiParameter(
                name="degree",
                description="Degree filter",
                required=False,
                enum=[choice.value for choice in Degree],
                type=str,
            ),
            OpenApiParameter(
                name="status",
                description="Status filter",
                required=False,
                type=bool,
            ),
            OpenApiParameter(
                name="search",
                description="Search term",
                required=False,
                type=str,
            ),
        ]
    )
    def get(self, request):
        queryset = self.get_queryset()
        is_contracted = request.query_params.get("is_contracted")
        degree = request.query_params.get("degree")
        status = request.query_params.get("status")
        search = request.query_params.get("search")
        if is_contracted is not None:
            try:
                is_contracted = is_contracted.lower() in ["true", "1", "yes"]
                queryset = queryset.filter(is_contracted=is_contracted)
            except (DRFValidationError, ValueError):
                queryset = queryset.all()
        if degree:
            try:
                queryset = queryset.filter(degree=degree)
            except (DRFValidationError, ValueError):
                queryset = queryset.all()
        if status is not None:
            try:
                status = status.lower() in ["true", "1", "yes"]
                queryset = queryset.filter(status=status)
            except (DRFValidationError, ValueError):
                queryset = queryset.all()
        if search:
            search_terms = search[:100].split()
            query = Q()
            for term in search_terms:
                query &= (
                    Q(user__first_name__icontains=term)
                    | Q(user__last_name__icontains=term)
                    | Q(user__father_name__icontains=term)
                    | Q(user__phone__icontains=term)
                )
            queryset = queryset.filter(query)
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ModeratorAdminSiteDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ModeratorAdminSiteSerializer

    def get_object(self, pk):
        try:
            return Moderator.objects.get(pk=pk)
        except Moderator.DoesNotExist:
            return None

    def get(self, request, pk):
        moderator = self.get_object(pk)
        if moderator is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(moderator)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        moderator = self.get_object(pk)
        if moderator is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(moderator, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
