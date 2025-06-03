from rest_framework import serializers

from apps.home.models.seo import Seo


class SeoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Seo model.
    """

    class Meta:
        model = Seo
        fields = (
            "id",
            "seo_type",
            "image",
            "title",
            "description",
            "keywords",
            "opengraph_title",
            "opengraph_description",
            "twitter_title",
            "twitter_description",
            "created_at",
        )
        read_only_fields = ("id",)
