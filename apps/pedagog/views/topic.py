from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pedagog.models.moderator import Moderator
from apps.pedagog.models.plan import Plan
from apps.pedagog.models.topic import Topic
from apps.pedagog.serializers.topic import TopicDetailSerializer, TopicSerializer, TopicAllDetailSerializer
from rest_framework.generics import get_object_or_404
from apps.shared.pagination.custom import CustomPagination


class TopicApiView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        plan_id = request.query_params.get("plan_id")
        search = request.query_params.get("search")

        if plan_id:
            topics = Topic.objects.filter(plan_id=plan_id)
            if search:
                topics = topics.filter(name__icontains=search)
            paginator = self.pagination_class()
            paginated_topics = paginator.paginate_queryset(topics, request)
            serializer = TopicDetailSerializer(
                paginated_topics, many=True, context={"request": request}
            )
            return paginator.get_paginated_response(serializer.data)

        return Response(
            {"error": "Either id or plan_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request):
        user = request.user
        try:
            moderator = Moderator.objects.get(user=user)
        except Moderator.DoesNotExist:
            return Response(
                {"error": "You are not a moderator"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not moderator.topic_creatable:
            return Response(
                {"error": "You are not allowed to create topic"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TopicSerializer(
            data=request.data, many=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        serializer = TopicAllDetailSerializer(topic, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        serializer = TopicSerializer(topic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
