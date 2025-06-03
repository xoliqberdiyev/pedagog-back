from rest_framework import serializers

from apps.pedagog.models.download import Download
from apps.pedagog.models.media import Media
from apps.pedagog.serializers.topic import ModeratorTopicSerializer


class UploadMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            "id",
            "topic_id",
            "name",
            "desc",
            "image",
            "type",
            "size",
            "view_count",
            "statistics",
            "created_at",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["topic_id"] = ModeratorTopicSerializer(instance.topic_id).data
        return representation


class DownloadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Download
        fields = (
            "id",
            "date",
            "media",
            "created_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["media"] = UploadMediaSerializer(instance.media).data
        return data
