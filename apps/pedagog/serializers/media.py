from rest_framework import serializers

from apps.pedagog.models.media import Media
from apps.pedagog.tasks.convert_file import convert_image_create
from apps.pedagog.serializers.converted_media import ConvertedMediaSerializer


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            "id",
            "topic_id",
            "desc",
            "file",
            "image",
            "media_type",
        )
        extra_kwargs = {"media_type": {"required": False}}
    
    def create(self, validated_data):
        file = validated_data.pop('file')
        media = Media.objects.create(file=file, **validated_data)

        # if file:
        #     convert_image_create.delay(media.id)

        return media


class MediaDetailSerializer(serializers.ModelSerializer):
    is_author = serializers.SerializerMethodField()
    converted_medias = ConvertedMediaSerializer(many=True)

    class Meta:
        model = Media
        fields = (
            "id",
            "name",
            "desc",
            "type",
            "size",
            "count",
            "statistics",
            "created_at",
            "view_count",
            "is_author", 
            "user",
            "converted_medias",
            "media_type"
        )

    def get_is_author(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        return obj.user == request.user

    def to_representation(self, instance):
        from apps.users.serializers.user import UserMiniSerializer

        data = super().to_representation(instance)
        request = self.context.get("request")
        data["user"] = UserMiniSerializer(instance.user).data
        if request and request.user.is_authenticated:
            data["is_author"] = instance.user == request.user

        return data


class MediaMiniSerializer(serializers.ModelSerializer):
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = (
            "id",
            "user",
            "name",
            "desc",
            "type",
            "size",
            "is_author",
            "view_count",
            "created_at",
        )

    def get_is_author(self, obj):
        return obj.user == self.context["request"].user
