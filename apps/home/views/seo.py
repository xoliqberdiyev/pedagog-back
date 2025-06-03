from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.home.models.seo import Seo, SeoType
from apps.home.serializers.seo import SeoSerializer
from apps.shared.pagination.custom import CustomPagination


class SeoView(APIView):
    serializer_class = SeoSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    queryset = Seo.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="type",
                description="Seo Type",
                required=True,
                type=str,
                enum=[i[0] for i in SeoType.choices],
            ),
        ],
        responses={
            200: SeoSerializer,
        },
    )
    def get(self, request):
        """
        Get all SEO objects.
        """
        type = request.query_params.get("type")
        queryset = self.queryset
        if type:
            queryset = queryset.filter(seo_type=type)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)
