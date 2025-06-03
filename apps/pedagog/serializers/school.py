from rest_framework import serializers

from apps.pedagog.models.school import SchoolType


class SchoolTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolType
        fields = (
            "id",
            "name",
            "created_at",
        )
        read_only_fields = ("id", "created_at")
