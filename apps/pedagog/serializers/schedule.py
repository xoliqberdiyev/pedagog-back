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
            "classes",
            "class_group",
            "science",
            "science_language",
            "weekday",
            "lesson_number",
            "start_time",
            "end_time",
            "color",
            "schedule_type",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at", "user")
