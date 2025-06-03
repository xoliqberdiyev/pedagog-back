from rest_framework import serializers

from apps.pedagog.models.ai import Ai


class AiSerializer(serializers.ModelSerializer):
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Ai
        fields = (
            "id",
            "type",
            "answer",
            "topic",
            "question",
            "is_author",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at", "is_author")

    def get_is_author(self, obj):
        return self.context["request"].user == obj.user

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data.pop("user", None)
        return Ai.objects.create(user=user, **validated_data)
