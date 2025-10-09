from django.contrib.auth.models import AnonymousUser
from django.db.models import OuterRef, Subquery, Q


from rest_framework import parsers, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pedagog.filters.electron_resource import ElectronResourceFilter
from apps.pedagog.models.electron_resource import (
    ElectronResource,
    ElectronResourceCategory,
    ElectronResourceSubCategory,
)
from apps.pedagog.serializers.electron_resource import (
    ElectronResourceAdminSerializer,
    ElectronResourceCategoryDetailSerializer,
    ElectronResourceCategorySerializer,
    ElectronResourceCreateSerializer,
    ElectronResourceSerializer,
    ElectronResourceSubCategorySerializer,
)
from apps.shared.pagination.custom import CustomPagination
from apps.users.choices.role import Role
from apps.payment.models.models import Orders


class ElectronResourceCategoryView(APIView):
    serializer_class = ElectronResourceCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request):
        search = request.query_params.get("search")
        queryset = ElectronResourceCategory.objects.filter(is_active=True)
        if search:
            search_terms = search[:100].split()
            query = Q()
            for term in search_terms:
                query &= Q(name__icontains=term) | Q(description__icontains=term)
            queryset = queryset.filter(query)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ElectronResourceCategoryDetailView(APIView):
    serializer_class = ElectronResourceCategoryDetailSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        category = get_object_or_404(ElectronResourceCategory, pk=pk)
        serializer = self.serializer_class(category)
        return Response(serializer.data)


class ElectronResourceSubCategoryView(APIView):
    serializer_class = ElectronResourceSubCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [IsAuthenticated()]
        elif self.request.method == "GET":
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request):
        queryset = ElectronResourceSubCategory.objects.filter(is_active=True)
        search = request.query_params.get("search")
        category = request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)
        if search:
            search_terms = search[:100].split()
            query = Q()
            for term in search_terms:
                query &= Q(name__icontains=term) | Q(description__icontains=term)
            queryset = queryset.filter(query)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        user = request.user
        if user.role != Role.MODERATOR and user.role != Role.ADMIN:
            return Response(
                {"error": "You are not allowed to create sub category"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElectronResourceSubCategoryDetailView(APIView):
    serializer_class = ElectronResourceSubCategorySerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAuthenticated()]
        elif self.request.method == "GET":
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, pk):
        sub_category = get_object_or_404(ElectronResourceSubCategory, pk=pk)
        serializer = self.serializer_class(sub_category)
        return Response(serializer.data)

    def patch(self, request, pk):
        sub_category = get_object_or_404(
            ElectronResourceSubCategory, pk=pk, user=request.user
        )
        serializer = self.serializer_class(sub_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElectronResourceView(GenericAPIView):
    serializer_class = ElectronResourceSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request):
        queryset = ElectronResource.objects.filter(is_active=True)
        search = request.query_params.get("search")
        category = request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)
        if search:
            search_terms = search[:100].split()
            query = Q()
            for term in search_terms:
                query &= Q(name__icontains=term) | Q(description__icontains=term)
            queryset = queryset.filter(query)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(
            result_page, many=True, context={"user": request.user}
        )
        return paginator.get_paginated_response(serializer.data)


class PaidElectronResourceView(GenericAPIView):
    serializer_class = ElectronResourceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        user = request.user
        latest_orders = Orders.objects.filter(
            electronic_resource=OuterRef('pk'),
            user=user
        ).order_by('-created_at')

        queryset = ElectronResource.objects.annotate(
            latest_status=Subquery(latest_orders.values('status')[:1])
        ).filter(latest_status=True)

        search = request.query_params.get("search")
        category = request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)
        if search:
            search_terms = search[:100].split()
            query = Q()
            for term in search_terms:
                query &= Q(name__icontains=term) | Q(description__icontains=term)
            queryset = queryset.filter(query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'user': user})
            return self.get_paginated_response(serializer.data)
        

class ElectronResourceCreateApiView(GenericAPIView):
    serializer_class = ElectronResourceCreateSerializer
    queryset = ElectronResource.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ElectronResourceDetailView(APIView):
    serializer_class = ElectronResourceSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAuthenticated()]
        elif self.request.method == "GET":
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, pk):
        resource = get_object_or_404(ElectronResource, pk=pk)
        serializer = self.serializer_class(resource)
        return Response(serializer.data)

    def patch(self, request, pk):
        resource = get_object_or_404(ElectronResource, pk=pk, user=request.user)
        serializer = self.serializer_class(resource, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElectronResourceAdminView(APIView):
    serializer_class = ElectronResourceAdminSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [IsAuthenticated()]
        elif self.request.method == "GET":
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request):
        queryset = ElectronResource.objects.filter(is_active=True)

        # 🧠 Filtering
        filterset = ElectronResourceFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        queryset = filterset.qs

        # 📊 Statistikalar
        user_count = queryset.values("user").distinct().count()
        file_count = queryset.count()
        file_type_count = queryset.values("type").distinct().count()
        file_size_count = queryset.values("size").distinct().count()
        file_create_count = queryset.values("created_at__date").distinct().count()
        category_count = queryset.values("category__category").distinct().count()
        sub_category_count = queryset.values("category").distinct().count()
        total_count = (
            user_count
            + file_count
            + file_type_count
            + file_size_count
            + file_create_count
            + category_count
            + sub_category_count
        )

        # ⏬ Pagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)

        response_data = {
            "data": serializer.data,
            "user_count": user_count,
            "file_count": file_count,
            "file_type_count": file_type_count,
            "file_size_count": file_size_count,
            "file_create_count": file_create_count,
            "category_count": category_count,
            "sub_category_count": sub_category_count,
            "total_count": total_count,
        }

        return paginator.get_paginated_response(response_data)
