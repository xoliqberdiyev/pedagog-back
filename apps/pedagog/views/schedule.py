from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pedagog.models.schedule import LessonSchedule, ScheduleType
from apps.pedagog.serializers.schedule import LessonScheduleSerializer
from apps.shared.pagination.custom import CustomPagination


class LessonScheduleView(APIView):
    serializer_class = LessonScheduleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Returns a queryset of LessonSchedule objects filtered by the current user's school.
        """
        user = self.request.user
        return LessonSchedule.objects.filter(user=user)

    def get(self, request):
        """
        Handles GET requests to retrieve the lesson schedule for the authenticated user.
        """
        schedule_type = request.query_params.get("schedule_type", None)
        queryset = self.get_queryset()
        if schedule_type and schedule_type == ScheduleType.SECOND_WEEK:
            queryset = queryset.filter(schedule_type=schedule_type)
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Handles POST requests to create a new lesson schedule entry.
        """
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonScheduleDetailView(APIView):
    serializer_class = LessonScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Handles GET requests to retrieve a specific lesson schedule entry.
        """
        lesson_schedule = get_object_or_404(LessonSchedule, pk=pk, user=request.user)
        serializer = self.serializer_class(lesson_schedule)
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        Handles PATCH requests to update a specific lesson schedule entry.
        """
        lesson_schedule = get_object_or_404(LessonSchedule, pk=pk, user=request.user)
        serializer = self.serializer_class(
            lesson_schedule, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handles DELETE requests to remove a specific lesson schedule entry.
        """
        lesson_schedule = get_object_or_404(LessonSchedule, pk=pk, user=request.user)
        lesson_schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
