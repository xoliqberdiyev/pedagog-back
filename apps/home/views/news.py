from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.home.models.news import NewsCategory, News
from apps.home.serializers.news import (
    NewsCategorySerializer,
    NewsSerializer,
    NewsDetailSerializer,
)
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination.custom import CustomPagination


class NewsCategoryListView(APIView):
    """
    API view to retrieve a list of news categories.
    """

    permission_classes = [AllowAny]
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    pagination_class = CustomPagination

    def get(self, request):
        """
        Handle GET requests to retrieve a list of news categories.
        """
        queryset = self.queryset
        paginator = self.pagination_class()
        paginated_categories = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_categories, many=True)
        return paginator.get_paginated_response(serializer.data)


class NewsListView(APIView):
    """
    API view to retrieve a list of news articles.
    """

    permission_classes = [AllowAny]
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = CustomPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search", description="Search term", required=False, type=str
            ),
            OpenApiParameter(
                name="category", description="Category ID", required=False, type=int
            ),
            OpenApiParameter(
                name="is_trending",
                description="Is trending filter",
                required=False,
                type=bool,
            ),
            OpenApiParameter(
                name="is_trending_banner",
                description="Is trending banner filter",
                required=False,
                type=bool,
            ),
            OpenApiParameter(
                name="is_popular",
                description="Is popular filter",
                required=False,
                type=bool,
            ),
            OpenApiParameter(
                name="is_popular_banner",
                description="Is popular banner filter",
                required=False,
                type=bool,
            ),
        ],
        responses={200: NewsSerializer(many=True)},
    )
    def get(self, request):
        """
        Handle GET requests to retrieve a list of news articles.
        """
        category = request.query_params.get("category")
        search = request.query_params.get("search")
        is_trending = request.query_params.get("is_trending")
        is_trending_banner = request.query_params.get("is_trending_banner")
        is_popular = request.query_params.get("is_popular")
        is_popular_banner = request.query_params.get("is_popular_banner")
        queryset = self.queryset

        if category and category.isdigit():
            queryset = queryset.filter(category__id=category)

        if search:
            search_terms = search[:100].split()
            query = Q()
            for term in search_terms:
                query &= (
                    Q(title__icontains=term)
                    | Q(title_uz__icontains=term)
                    | Q(title_ru__icontains=term)
                    | Q(title_en__icontains=term)
                    | Q(short_title__icontains=term)
                    | Q(short_title_uz__icontains=term)
                    | Q(short_title_ru__icontains=term)
                    | Q(content__icontains=term)
                    | Q(content_uz__icontains=term)
                    | Q(content_ru__icontains=term)
                    | Q(content_en__icontains=term)
                )
            queryset = queryset.filter(query)

        if is_trending and is_trending.lower() == "true":
            queryset = queryset.filter(is_trending=True)

        if is_trending_banner and is_trending_banner.lower() == "true":
            queryset = queryset.filter(is_trending=True)[:1]

        if is_popular and is_popular.lower() == "true":
            queryset = queryset.order_by("-view_count")

        if is_popular_banner and is_popular_banner.lower() == "true":
            queryset = queryset.order_by("-view_count")[:1]

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class NewsDetailView(APIView):
    """
    API view to retrieve a single news article.
    """

    permission_classes = [AllowAny]
    serializer_class = NewsDetailSerializer

    def get(self, request, pk):
        """
        Handle GET requests to retrieve a single news article.
        """
        queryset = get_object_or_404(News, pk=pk)
        queryset.increment_views()
        serializer = self.serializer_class(queryset)
        return Response(
            {
                "success": True,
                "message": "Data fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
