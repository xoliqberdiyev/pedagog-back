from rest_framework import serializers

from apps.pedagog.models.science import Science, ScienceLanguage


class ScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = (
            "id",
            "name",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class ScienceLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScienceLanguage
        fields = (
            "id",
            "name",
            "created_at",
        )
        read_only_fields = ("id", "created_at")
