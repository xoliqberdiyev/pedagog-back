from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pedagog.models.moderator import Moderator
from apps.pedagog.models.plan import Plan
from apps.pedagog.models.topic import Topic
from apps.pedagog.serializers.topic import TopicDetailSerializer, TopicSerializer
from apps.shared.pagination.custom import CustomPagination


class TopicApiView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        plan_id = request.query_params.get("plan_id")
        topic_id = request.query_params.get("id")
        search = request.query_params.get("search")

        if topic_id:
            try:
                topic = Topic.objects.get(id=topic_id)
                topic.view_count += 1
                topic.save(update_fields=["view_count"])
                for media in topic.medias.all():
                    media.calculation_view_count()
                serializer = TopicDetailSerializer(topic, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Topic.DoesNotExist:
                return Response(
                    {"error": "Topic not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        if plan_id:
            try:
                topics = Topic.objects.filter(plan_id=plan_id)
                if search:
                    topics = topics.filter(name__icontains=search)
                paginator = self.pagination_class()
                paginated_topics = paginator.paginate_queryset(topics, request)
                serializer = TopicDetailSerializer(
                    paginated_topics, many=True, context={"request": request}
                )
                return paginator.get_paginated_response(serializer.data)
            except Plan.DoesNotExist:
                return Response(
                    {"error": "Plan not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {"error": "Either id or plan_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request):
        user = request.user
        plan_id = (
            request.data[0].get("plan_id")
            if isinstance(request.data, list)
            else request.data.get("plan_id")
        )
        if not plan_id:
            return Response(
                {"error": "plan_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response(
                {"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND
            )

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
            serializer.save(plan_id=plan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        topic_id = request.query_params.get("id")
        if not topic_id:
            return Response(
                {"error": "id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response(
                {"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TopicSerializer(topic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
