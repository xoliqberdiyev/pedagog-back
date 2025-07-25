from rest_framework import serializers

from apps.pedagog.models.media_type import MediaType


class MediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaType
        fields = [
            'id', 'name'
        ]