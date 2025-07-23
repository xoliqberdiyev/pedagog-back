from rest_framework import serializers

from apps.pedagog.models.converted_media import ConvertedMedia


class ConvertedMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvertedMedia
        fields = [
            'id', 
            'image',
            'page_number',
        ]