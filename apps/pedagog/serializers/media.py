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
            "view_count",
            "is_author",
            "user",
        )

    def get_is_author(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        return obj.user == request.user

    def to_representation(self, obj):
        from apps.users.serializers.user import UserMiniSerializer
        data = super().to_representation(obj)
        request = self.context.get("request")
        data["user"] = UserMiniSerializer(obj.user).data
        if request and request.user.is_authenticated:
            data["is_author"] = obj.user == request.user

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
