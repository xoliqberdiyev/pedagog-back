from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pedagog.models.media import Media
from apps.pedagog.models.topic import Topic
from apps.pedagog.serializers.media import MediaDetailSerializer, MediaSerializer
from apps.users.views.locations import CustomPagination


class MediaApiView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        media_id = request.query_params.get("id")
        topic_id = request.query_params.get("topic_id")

        if media_id:
            try:
                media = Media.objects.get(id=media_id)
                serializer = MediaDetailSerializer(media, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Media.DoesNotExist:
                return Response(
                    {"error": "Media not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        if topic_id:
            try:
                media = Media.objects.filter(topic_id=topic_id)
                paginator = self.pagination_class()
                paginated_media = paginator.paginate_queryset(media, request)
                serializer = MediaDetailSerializer(
                    paginated_media, many=True, context={"request": request}
                )
                return paginator.get_paginated_response(serializer.data)
            except Topic.DoesNotExist:
                return Response(
                    {"error": "Topic not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {"error": "media_id is required"},
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

    def delete(self, request):
        media_id = request.query_params.get("id")
        if not media_id:
            return Response(
                {"error": "media_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            media = Media.objects.get(id=media_id, user=request.user)
        except Media.DoesNotExist:
            return Response(
                {"error": "Media not found"}, status=status.HTTP_404_NOT_FOUND
            )

        media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request):
        media_id = request.query_params.get("id")
        if not media_id:
            return Response(
                {"error": "media_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            media = Media.objects.get(id=media_id)
        except Media.DoesNotExist:
            return Response(
                {"error": "Media not found"}, status=status.HTTP_404_NOT_FOUND
            )

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
