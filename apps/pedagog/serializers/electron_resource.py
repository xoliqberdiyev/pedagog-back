from rest_framework import serializers

from apps.pedagog.models.electron_resource import (
    SeoMetaCategoryData,
    SeoOgCategoryData,
    SeoTwitterCategoryData,
    ElectronResourceCategory,
    ElectronResourceSubCategory,
    ElectronResource,
)


class SeoMetaCategoryDataSerializer(serializers.ModelSerializer):
    """
    Serializer for SEO metadata of Category model.
    """

    class Meta:
        model = SeoMetaCategoryData
        fields = (
            "id",
            "category",
            "title",
            "description",
            "keywords",
            "canonical_url",
        )
        read_only_fields = ("id",)


class SeoOgCategoryDataSerializer(serializers.ModelSerializer):
    """
    Serializer for Open Graph metadata of Category model.
    """

    class Meta:
        model = SeoOgCategoryData
        fields = (
            "id",
            "category",
            "og_title",
            "og_description",
            "og_image",
        )
        read_only_fields = ("id",)


class SeoTwitterCategoryDataSerializer(serializers.ModelSerializer):
    """
    Serializer for Twitter Card metadata of Category model.
    """

    class Meta:
        model = SeoTwitterCategoryData
        fields = (
            "id",
            "category",
            "twitter_card",
            "twitter_title",
            "twitter_description",
            "twitter_image",
        )
        read_only_fields = ("id",)


class ElectronResourceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronResourceCategory
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "first_color",
            "second_color",
            "created_at",
        )


class ElectronResourceCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronResourceCategory
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "first_color",
            "second_color",
            "created_at",
        )

    def to_representation(self, instance):
        """
        Customize the representation of the Category model.
        """
        representation = super().to_representation(instance)
        representation["meta"] = (
            SeoMetaCategoryDataSerializer(instance.seo_meta).data
            if hasattr(instance, "seo_meta") and instance.seo_meta is not None
            else []
        )
        representation["og"] = (
            SeoOgCategoryDataSerializer(instance.og_meta).data
            if hasattr(instance, "og_meta") and instance.og_meta is not None
            else []
        )
        representation["twitter"] = (
            SeoTwitterCategoryDataSerializer(instance.twitter_meta).data
            if hasattr(instance, "twitter_meta") and instance.twitter_meta is not None
            else []
        )
        return representation


class ElectronResourceSubCategoryMiniSerializer(serializers.ModelSerializer):
    category = ElectronResourceCategorySerializer()

    class Meta:
        model = ElectronResourceSubCategory
        fields = (
            "id",
            "name",
            "description",
            "category",
            "created_at",
        )


class ElectronResourceSubCategorySerializer(serializers.ModelSerializer):
    category = ElectronResourceCategorySerializer()

    class Meta:
        model = ElectronResourceSubCategory
        fields = (
            "id",
            "name",
            "description",
            "category",
            "created_at",
        )
        extra_kwargs = {"user": {"required": False}}


class ElectronResourceSerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = ElectronResource
        fields = (
            "id",
            "user",
            "description",
            "file",
            "name",
            "size",
            "type",
            "category",
            "sub_categories",
            "created_at",
        )
        extra_kwargs = {
            "name": {"required": False},
            "size": {"required": False},
            "type": {"required": False},
            "user": {"required": False},
        }

    def get_sub_categories(self, obj):
        if isinstance(obj.category, ElectronResourceCategory):
            sub_categories = ElectronResourceSubCategory.objects.filter(
                category=obj.category
            )
            return ElectronResourceSubCategorySerializer(sub_categories, many=True).data
        return []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        from apps.users.serializers.user import UserSerializer

        data["user"] = UserSerializer(instance.user).data
        return data


class ElectronResourceMiniSerializer(serializers.ModelSerializer):
    sub_category = ElectronResourceSubCategoryMiniSerializer(source="category")

    class Meta:
        model = ElectronResource
        fields = (
            "id",
            "file",
            "name",
            "description",
            "sub_category",
            "created_at",
        )


class ElectronResourceAdminSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    sub_category = ElectronResourceSubCategoryMiniSerializer(source="category")

    class Meta:
        model = ElectronResource
        fields = (
            "id",
            "user",
            "name",
            "size",
            "type",
            "category",
            "sub_category",
            "created_at",
        )

    def get_user(self, obj):
        from apps.users.serializers.user import UserSerializer

        user = UserSerializer(obj.user).data

        return {
            "id": user["id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
        }



class ElectronResourceSubCategorySearchSerializer(serializers.ModelSerializer):
    category = ElectronResourceCategorySerializer()

    class Meta:
        model = ElectronResourceSubCategory
        fields = (
            "id",
            "name",
            "description",
            'category',
            "created_at",
        )
        extra_kwargs = {"user": {"required": False}}


class ElectronResourceSearchSerializer(serializers.ModelSerializer):
    category = ElectronResourceSubCategorySerializer()

    class Meta:
        model = ElectronResource
        fields = (
            "id",
            "name",
            "description",
            "category",
            'file',
            'price',
            "created_at",
        )