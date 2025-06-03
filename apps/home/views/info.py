from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.home.models.info import PedagogInfo
from apps.home.serializers.info import PedagogInfoSerializer
from apps.shared.pagination.custom import CustomPagination


class PedagogInfoListView(APIView):
    """
    API view to retrieve a list of pedagog information.
    """

    permission_classes = [AllowAny]
    queryset = PedagogInfo.objects.all()
    serializer_class = PedagogInfoSerializer
    pagination_class = CustomPagination

    def get(self, request):
        """
        Handle GET requests to retrieve a list of pedagog information.
        """
        queryset = self.queryset
        paginator = self.pagination_class()
        paginated_info = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_info, many=True)
        return paginator.get_paginated_response(serializer.data)
