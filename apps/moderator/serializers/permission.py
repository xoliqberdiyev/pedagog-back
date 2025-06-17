from rest_framework import serializers

from apps.moderator.models.permission import ModeratorPermission
from apps.pedagog.serializers.classes import ClassesSerializer
from apps.pedagog.serializers.school import SchoolTypeSerializer
from apps.pedagog.serializers.science import ScienceSerializer


class ModeratorPermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for ModeratorPermission model.
    """

    class Meta:
        model = ModeratorPermission
        fields = (
            "id",
            "user",
            "status",
            "school_type",
            "classes",
            "science",
            "science_language",
            "created_at",
        )
        read_only_fields = ("id", "created_at")
        extra_kwargs = {
            "user": {"read_only": True},
            "status": {"read_only": True},
        }

    def to_representation(self, instance):
        """
        Custom representation to include user details.
        """
        representation = super().to_representation(instance)
        representation["school_type"] = SchoolTypeSerializer(instance.school_type, many=True).data
        representation["classes"] = ClassesSerializer(instance.classes, many=True).data
        representation["science"] = ScienceSerializer(instance.science, many=True).data
        representation["science_language"] = ScienceSerializer(instance.science_language, many=True).data
        return representation
