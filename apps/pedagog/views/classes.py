from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.pedagog.models.classes import Classes
from apps.pedagog.serializers.classes import ClassesSerializer
from apps.shared.pagination.custom import CustomPagination


class ClassesListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassesSerializer
    queryset = Classes.objects.filter(is_active=True)
    pagination_class = CustomPagination

    def get(self, request):
        school_type = request.query_params.get("school_type", None)
        queryset = self.queryset
        if school_type:
            queryset = queryset.filter(school_types__id=int(school_type))
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
