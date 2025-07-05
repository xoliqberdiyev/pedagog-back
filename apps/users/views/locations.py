from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.users.serializers.locations import RegionSerializer, DistrictSerializer
from apps.shared.pagination.custom import CustomPagination
from apps.users.models.locations import Region, District


class RegionAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegionSerializer
    pagination_class = None
    queryset = Region.objects.all()

    def get(self, request):
        return self.serializer_class(self.queryset, many=True).data


class DistrictAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = DistrictSerializer
    pagination_class = None
    queryset = District.objects.all()

    def get(self, request):
        region = request.query_params.get("region", None)
        queryset = self.queryset
        if region:
            queryset = queryset.filter(region=int(region))
        return self.serializer_class(queryset, many=True).data
