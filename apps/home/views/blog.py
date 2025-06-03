from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.home.models.blog import BlogCategory, Blog
from apps.home.serializers.blog import (
    BlogCategorySerializer,
    BlogSerializer,
    BlogDetailSerializer,
)
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination.custom import PedagogPagination


class BlogCategoryListView(APIView):
    """
    API view to retrieve a list of blog categories.
    """

    permission_classes = [AllowAny]
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    pagination_class = PedagogPagination

    def get(self, request):
        """
        Handle GET requests to retrieve a list of blog categories.
        """
        queryset = self.queryset
        paginator = self.pagination_class()
        paginated_categories = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_categories, many=True)
        return paginator.get_paginated_response(serializer.data)


class BlogListView(APIView):
    """
    API view to retrieve a list of blog articles.
    """

    permission_classes = [AllowAny]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = PedagogPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search", description="Search term", required=False, type=str
            ),
            OpenApiParameter(
                name="category", description="Category ID", required=False, type=int
            ),
        ],
        responses={200: BlogSerializer(many=True)},
    )
    def get(self, request):
        """
        Handle GET requests to retrieve a list of blog articles.
        """
        category = request.query_params.get("category")
        search = request.query_params.get("search")
        queryset = self.queryset

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

        if category and category.isdigit():
            queryset = queryset.filter(category__id=category)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class BlogDetailView(APIView):
    """
    API view to retrieve a single blog article.
    """

    permission_classes = [AllowAny]
    serializer_class = BlogDetailSerializer

    def get(self, request, pk):
        """
        Handle GET requests to retrieve a single blog article.
        """
        blog = get_object_or_404(Blog, pk=pk)
        serializer = self.serializer_class(blog)
        return Response(
            {
                "success": True,
                "message": "Data fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
