from rest_framework import serializers

from apps.pedagog.models.tmr_appeal import TMRAppeal, TmrFiles


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
            "science",
            "science_type",
            "classes",
            "class_groups",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["status"]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["status"] = instance.status
        context["science"] = instance.science.name
        context["science_type"] = instance.science_type.name
        context["classes"] = instance.classes.name
        context["class_groups"] = instance.class_groups.name
        context["files"] = TmrFilesSerializer(instance.files.all(), many=True).data
        return context

    def create(self, validated_data):
        return TMRAppeal.objects.create(
            **validated_data, user=self.context["request"].user
        )
