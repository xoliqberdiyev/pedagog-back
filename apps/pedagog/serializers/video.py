from rest_framework import serializers

from apps.pedagog.models.video import VideoModel


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoModel
        fields = [
            "id",
            "title",
            "desc",
            "duration",
            "badge_title",
            "badge_color",
        ]
