from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.pedagog.models.school import SchoolType
from apps.pedagog.serializers.school import SchoolTypeSerializer
from apps.shared.pagination.custom import CustomPagination


class SchoolTypeListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolTypeSerializer
    queryset = SchoolType.objects.filter(is_active=True)
    pagination_class = CustomPagination

    def get(self, request):
        queryset = self.queryset
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
