from rest_framework import serializers

from apps.pedagog.models.tmr_appeal import TMRAppeal, TmrFiles
from apps.pedagog.serializers.classes import ClassesSerializer
from apps.pedagog.serializers.school import SchoolTypeSerializer
from apps.pedagog.serializers.science import ScienceSerializer, ScienceLanguageSerializer


class TmrFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmrFiles
        fields = (
            "id",
            "tmr_appeal",
            "title",
            "description",
            "file",
            "is_active",
            "type",
            "size",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["type", "size"]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["url"] = instance.file.url
        return context


class TMRAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = TMRAppeal
        fields = (
            "id",
            "status",
            "school_type",
            "classes",
            "science",
            "science_language",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["status"]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["status"] = instance.status
        context["school_type"] = SchoolTypeSerializer(instance.school_type).data
        context["classes"] = ClassesSerializer(instance.classes).data
        context["science"] = ScienceSerializer(instance.science).data
        context["science_language"] = ScienceLanguageSerializer(instance.science_language).data
        context["files"] = TmrFilesSerializer(instance.files.all(), many=True).data
        return context

    def create(self, validated_data):
        return TMRAppeal.objects.create(
            **validated_data, user=self.context["request"].user
        )
