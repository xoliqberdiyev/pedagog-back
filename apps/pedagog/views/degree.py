from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.pedagog.models.degree import Degree
from apps.pedagog.serializers.degree import DegreeSerializer
from apps.shared.pagination.custom import CustomPagination


class DegreeListView(APIView):
    """
    API view to list all degrees.
    """

    serializer_class = DegreeSerializer
    permission_classes = (AllowAny,)
    queryset = Degree.objects.all()
    pagination_class = CustomPagination

    def get(self, request):
        """
        Handle GET requests to retrieve a list of price.
        """
        queryset = self.queryset
        paginator = self.pagination_class()
        paginated_categories = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_categories, many=True)
        return paginator.get_paginated_response(serializer.data)
