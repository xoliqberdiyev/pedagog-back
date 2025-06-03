from rest_framework import serializers

from apps.pedagog.models.media import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            "id",
            "topic_id",
            "desc",
            "file",
            "image",
        )


class MediaDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

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
            "user",
            "view_count",
            "is_author",
        )

    def get_user(self, obj):
        from apps.users.serializers.user import UserSerializer

        return UserSerializer(obj.user).data

    def get_is_author(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        return obj.user == request.user


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
