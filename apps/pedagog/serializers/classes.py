from rest_framework import serializers

from apps.pedagog.models.classes import Classes


class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = (
            "id",
            "name",
            "created_at",
        )
        read_only_fields = ("id", "created_at")
