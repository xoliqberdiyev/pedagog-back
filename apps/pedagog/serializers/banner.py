from rest_framework import serializers

from apps.pedagog.models.banner import BannerModel


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = BannerModel
        fields = [
            "id",
            "title",
            "description",
            "image",
            "button_title",
            "button_link",
        ]
