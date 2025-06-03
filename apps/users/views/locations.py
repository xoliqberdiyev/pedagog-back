from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.users.serializers.locations import RegionSerializer, DistrictSerializer
from apps.shared.pagination.custom import CustomPagination
from apps.users.models.locations import Region, District


class RegionAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegionSerializer
    pagination_class = CustomPagination
    queryset = Region.objects.all()

    def get(self, request):
        queryset = self.queryset
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class DistrictAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = DistrictSerializer
    pagination_class = CustomPagination
    queryset = District.objects.all()

    def get(self, request):
        region = request.query_params.get("region", None)
        queryset = self.queryset
        if region:
            queryset = queryset.filter(region=int(region))
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
