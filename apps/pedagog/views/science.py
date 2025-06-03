from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.pedagog.models.science import Science, ScienceLanguage
from apps.pedagog.serializers.science import (
    ScienceSerializer,
    ScienceLanguageSerializer,
)
from apps.shared.pagination.custom import CustomPagination


class ScienceListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScienceSerializer
    queryset = Science.objects.filter(is_active=True)
    pagination_class = CustomPagination

    def get(self, request):
        classes = request.query_params.get("classes", None)
        queryset = self.queryset
        if classes:
            queryset = queryset.filter(classes__id=int(classes))
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class ScienceLanguageListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScienceLanguageSerializer
    queryset = ScienceLanguage.objects.filter(is_active=True)
    pagination_class = CustomPagination

    def get(self, request):
        science = request.query_params.get("science", None)
        queryset = self.queryset
        if science:
            queryset = queryset.filter(sciences__id=int(science))
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
