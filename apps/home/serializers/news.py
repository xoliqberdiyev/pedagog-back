from rest_framework import serializers

from apps.home.models.news import (
    NewsCategory,
    SeoMetaNewsData,
    SeoOgNewsData,
    SeoTwitterNewsData,
    News,
)


class NewsCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the NewsCategory model.
    """

    class Meta:
        model = NewsCategory
        fields = (
            "id",
            "name",
            "created_at",
        )
        read_only_fields = ("created_at",)


class SeoMetaNewsDataSerializer(serializers.ModelSerializer):
    """
    Serializer for SEO metadata of the News model.
    """

    class Meta:
        model = SeoMetaNewsData
        fields = (
            "id",
            "title",
            "description",
            "keywords",
            "canonical_url",
        )


class SeoOgNewsDataSerializer(serializers.ModelSerializer):
    """
    Serializer for Open Graph metadata of the News model.
    """

    class Meta:
        model = SeoOgNewsData
        fields = (
            "id",
            "og_title",
            "og_description",
            "og_image",
        )


class SeoTwitterNewsDataSerializer(serializers.ModelSerializer):
    """
    Serializer for Twitter Card metadata of the News model.
    """

    class Meta:
        model = SeoTwitterNewsData
        fields = (
            "id",
            "twitter_card",
            "twitter_title",
            "twitter_description",
            "twitter_image",
        )


class NewsSerializer(serializers.ModelSerializer):
    """
    Serializer for the News model.
    """

    class Meta:
        model = News
        fields = (
            "id",
            "title",
            "short_title",
            "reading_time",
            "image",
            "view_count",
            "created_at",
        )
        read_only_fields = ("created_at",)

    def to_representation(self, instance):
        """
        Customize the representation of the News model.
        """
        representation = super().to_representation(instance)
        representation["category"] = (
            NewsCategorySerializer(instance.category).data
            if hasattr(instance, "category") and instance.category is not None
            else []
        )
        return representation


class NewsDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed view of the News model.
    """

    class Meta:
        model = News
        fields = (
            "id",
            "title",
            "short_title",
            "reading_time",
            "content",
            "image",
            "view_count",
            "created_at",
        )
        read_only_fields = ("created_at",)

    def to_representation(self, instance):
        """
        Customize the representation of the News model.
        """
        representation = super().to_representation(instance)
        representation["category"] = (
            NewsCategorySerializer(instance.category).data
            if hasattr(instance, "category") and instance.category is not None
            else []
        )
        representation["meta"] = (
            SeoMetaNewsDataSerializer(instance.seo_meta).data
            if hasattr(instance, "seo_meta") and instance.seo_meta is not None
            else []
        )
        representation["og"] = (
            SeoOgNewsDataSerializer(instance.og_meta).data
            if hasattr(instance, "og_meta") and instance.og_meta is not None
            else []
        )
        representation["twitter"] = (
            SeoTwitterNewsDataSerializer(instance.twitter_meta).data
            if hasattr(instance, "twitter_meta") and instance.twitter_meta is not None
            else []
        )
        return representation
