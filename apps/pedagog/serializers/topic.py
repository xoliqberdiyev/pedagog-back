from rest_framework import serializers

from apps.pedagog.models.topic import Topic
from apps.pedagog.serializers.media import MediaDetailSerializer
from apps.pedagog.serializers.plan import PlanMiniSerializer


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [
            "id",
            "plan_id",
            "name",
            "description",
            "hours",
            "weeks",
            "sequence_number",
            "banner",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        topic = Topic.objects.create(**validated_data, user=user)
        return topic


class ModeratorTopicSerializer(serializers.ModelSerializer):
    plan = PlanMiniSerializer(source="plan_id")

    class Meta:
        model = Topic
        fields = [
            "id",
            "name",
            "description",
            "hours",
            "weeks",
            "sequence_number",
            "banner",
            "plan",
        ]

    def get_banner(self, obj):
        return obj.banner.url if obj.banner else None


class TopicDetailSerializer(serializers.ModelSerializer):
    media_count = serializers.SerializerMethodField()
    download_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = [
            "id",
            "name",
            "description",
            "hours",
            "sequence_number",
            "created_at",
            "weeks",
            "banner",
            "view_count",
            "media_count",
            "download_count",
        ]

    def get_media_count(self, obj):
        return obj.media_count

    def get_download_count(self, obj):
        return obj.all_download_count


class TopicAllDetailSerializer(serializers.ModelSerializer):
    media_count = serializers.SerializerMethodField()
    download_count = serializers.SerializerMethodField()
    plan_id = PlanMiniSerializer()

    class Meta:
        model = Topic
        fields = [
            "id",
            "plan_id",
            "name",
            "description",
            "hours",
            "sequence_number",
            "created_at",
            "weeks",
            "banner",
            "view_count",
            "media_count",
            "download_count",
        ]

    def get_media_count(self, obj):
        return obj.media_count

    def get_download_count(self, obj):
        return obj.all_download_count

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation["plan_id"] = PlanMiniSerializer(
    #         instance.plan_id, context=self.context
    #     ).data
    #     return representation


class MobileTopicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [
            "id",
            "plan_id",
            "name",
            "description",
            "hours",
            "sequence_number",
            "created_at",
            "weeks",
            "banner",
        ]


class TopicAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [
            "id",
            "name",
            "hours",
            "sequence_number",
            "created_at",
            "weeks",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["media"] = MediaDetailSerializer(
            instance.medias.all(), many=True, context=self.context
        ).data
        return representation
