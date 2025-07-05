from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.users.serializers.locations import RegionSerializer, DistrictSerializer
from apps.users.models.locations import Region, District
from rest_framework.response import Response
from apps.shared.pagination.custom import CustomPagination


class RegionAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegionSerializer

    def get(self, request):
        queryset = Region.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class DistrictAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = DistrictSerializer

    def get(self, request):
        region = request.query_params.get("region", None)
        queryset = District.objects.all()
        if region:
            queryset = queryset.filter(region=int(region))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

