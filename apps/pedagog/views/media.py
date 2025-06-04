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
        media_id = request.query_params.get("id")
        topic_id = request.query_params.get("topic_id")

        if media_id:
            media = get_object_or_404(Media, pk=media_id)
            serializer = MediaDetailSerializer(media, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        if topic_id:
            media = Media.objects.filter(topic_id=topic_id)
            paginator = self.pagination_class()
            paginated_media = paginator.paginate_queryset(media, request)
            serializer = MediaDetailSerializer(
                paginated_media, many=True, context={"request": request}
            )
            return paginator.get_paginated_response(serializer.data)

        return Response(
            {"error": "media_id or topic_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request):
        topic_id = request.query_params.get("topic_id")
        if not topic_id:
            return Response(
                {"error": "topic_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = MediaSerializer(
            data=request.data,
            context={"rq": request},
        )
        if serializer.is_valid():
            serializer.save(topic_id_id=topic_id, user=request.user, object_id=topic_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        media_id = request.query_params.get("id")
        if not media_id:
            return Response(
                {"error": "media_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        media = get_object_or_404(Media, pk=media_id)

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
