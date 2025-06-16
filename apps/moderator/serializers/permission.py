from rest_framework import serializers

from apps.moderator.models.permission import ModeratorPermission


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
