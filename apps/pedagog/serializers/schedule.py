from rest_framework import serializers

from apps.pedagog.models.schedule import LessonSchedule
from apps.pedagog.serializers.quarter import QuarterMiniSerializer
from apps.pedagog.serializers.classes import ClassesSerializer, ClassGroupSerializer
from apps.pedagog.serializers.science import ScienceSerializer, ScienceLanguageSerializer


class LessonScheduleSerializer(serializers.ModelSerializer):
    quarter = QuarterMiniSerializer()
    classes = ClassesSerializer()
    class_group = ClassGroupSerializer()
    science = ScienceSerializer()
    science_language = ScienceLanguageSerializer()

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
