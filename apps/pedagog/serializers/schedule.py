from rest_framework import serializers

from apps.pedagog.models.schedule import LessonSchedule


class LessonScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonSchedule
        fields = (
            "id",
            "user",
            "quarter",
            "shift",
            "topic",
            "classes",
            "class_group",
            "science",
            "science_language",
            "weekday",
            "lesson_number",
            "date",
            "start_time",
            "end_time",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at", "user")
