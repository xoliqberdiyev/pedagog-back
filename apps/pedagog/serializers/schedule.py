from rest_framework import serializers

from apps.pedagog.models.schedule import LessonSchedule
from apps.pedagog.serializers.quarter import QuarterMiniSerializer
from apps.pedagog.serializers.classes import ClassesSerializer, ClassGroupSerializer
from apps.pedagog.serializers.science import (
    ScienceSerializer,
    ScienceLanguageSerializer,
)


class LessonScheduleSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["quarter"] = QuarterMiniSerializer(instance.quarter).data
        data["classes"] = ClassesSerializer(instance.classes).data
        data["class_group"] = ClassGroupSerializer(instance.class_group).data
        data["science"] = ScienceSerializer(instance.science).data
        data["science_language"] = ScienceLanguageSerializer(
            instance.science_language
        ).data
        return data

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
