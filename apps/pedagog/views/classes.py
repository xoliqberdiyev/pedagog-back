from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView

from apps.pedagog.models.classes import Classes, ClassGroup
from apps.pedagog.serializers.classes import ClassesSerializer, ClassGroupSerializer
from apps.shared.pagination.custom import CustomPagination


class ClassesListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ClassesSerializer
    queryset = Classes.objects.filter(is_active=True).order_by('id')
    pagination_class = CustomPagination

    def get(self, request):
        school_type = request.query_params.get("school_type", None)
        search = request.query_params.get("search", None)
        queryset = self.queryset
        if school_type:
            queryset = queryset.filter(school_types__id=int(school_type))
        if search:
            queryset = queryset.filter(name__istartswith=search)
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class ClassGroupListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ClassGroupSerializer
    queryset = ClassGroup.objects.all()
    pagination_class = CustomPagination

    def get(self, request):
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(self.queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
