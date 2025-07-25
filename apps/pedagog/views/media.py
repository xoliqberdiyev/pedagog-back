from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pedagog.models.media import Media
from apps.pedagog.serializers.media import MediaDetailSerializer, MediaSerializer
from apps.users.views.locations import CustomPagination


class MediaApiView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        topic_id = request.query_params.get("topic_id")

        if topic_id:
            media = Media.objects.filter(topic_id=topic_id).prefetch_related('converted_medias').select_related('media_type')
            paginator = self.pagination_class()
            paginated_media = paginator.paginate_queryset(media, request)
            serializer = MediaDetailSerializer(
                paginated_media, many=True, context={"request": request}
            )
            return paginator.get_paginated_response(serializer.data)

        return Response(
            {"error": "topic_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request):
        serializer = MediaSerializer(
            data=request.data,
            context={"rq": request},
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediaDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        media = get_object_or_404(Media, pk=pk)
        media.calculation_view_count()
        serializer = MediaDetailSerializer(media, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        media = get_object_or_404(Media, pk=pk, user=request.user)
        serializer = MediaSerializer(
            media,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
