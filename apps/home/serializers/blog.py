from rest_framework import serializers

from apps.home.models.blog import (
    SeoMetaBlogData,
    SeoOgBlogData,
    SeoTwitterBlogData,
    BlogCategory,
    Blog,
)


class SeoMetaBlogDataSerializer(serializers.ModelSerializer):
    """
    Serializer for SEO metadata of Blog model.
    """

    class Meta:
        model = SeoMetaBlogData
        fields = (
            "id",
            "blog",
            "title",
            "description",
            "keywords",
            "canonical_url",
        )
        read_only_fields = ("id",)


class SeoOgBlogDataSerializer(serializers.ModelSerializer):
    """
    Serializer for Open Graph metadata of Blog model.
    """

    class Meta:
        model = SeoOgBlogData
        fields = (
            "id",
            "blog",
            "og_title",
            "og_description",
            "og_image",
        )
        read_only_fields = ("id",)


class SeoTwitterBlogDataSerializer(serializers.ModelSerializer):
    """
    Serializer for Twitter Card metadata of Blog model.
    """

    class Meta:
        model = SeoTwitterBlogData
        fields = (
            "id",
            "blog",
            "twitter_card",
            "twitter_title",
            "twitter_description",
            "twitter_image",
        )
        read_only_fields = ("id",)


class BlogCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for BlogCategory model.
    """

    class Meta:
        model = BlogCategory
        fields = (
            "id",
            "name",
            "created_at",
        )
        read_only_fields = ("created_at",)


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model.
    """

    class Meta:
        model = Blog
        fields = (
            "id",
            "title",
            "short_title",
            "image",
            "reading_time",
            "created_at",
        )
        read_only_fields = ("created_at",)

    def to_representation(self, instance):
        """
        Customize the representation of the Blog model.
        """
        representation = super().to_representation(instance)
        representation["category"] = (
            BlogCategorySerializer(instance.category).data
            if hasattr(instance, "category") and instance.category is not None
            else []
        )
        return representation


class BlogDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model with detailed information.
    """

    class Meta:
        model = Blog
        fields = (
            "id",
            "title",
            "short_title",
            "content",
            "image",
            "reading_time",
            "created_at",
        )
        read_only_fields = ("created_at",)

    def to_representation(self, instance):
        """
        Customize the representation of the Blog model.
        """
        representation = super().to_representation(instance)
        representation["category"] = (
            BlogCategorySerializer(instance.category).data
            if hasattr(instance, "category") and instance.category is not None
            else []
        )
        representation["meta"] = (
            SeoMetaBlogDataSerializer(instance.seo_meta).data
            if hasattr(instance, "seo_meta") and instance.seo_meta is not None
            else []
        )
        representation["og"] = (
            SeoOgBlogDataSerializer(instance.og_meta).data
            if hasattr(instance, "og_meta") and instance.og_meta is not None
            else []
        )
        representation["twitter"] = (
            SeoTwitterBlogDataSerializer(instance.twitter_meta).data
            if hasattr(instance, "twitter_meta") and instance.twitter_meta is not None
            else []
        )
        return representation
