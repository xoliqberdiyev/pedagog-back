from rest_framework import serializers

from apps.pedagog.models.media import Media
from apps.pedagog.models.plan import Plan
from apps.pedagog.models.topic import Topic
from apps.pedagog.serializers.classes import ClassesSerializer
from apps.pedagog.serializers.quarter import QuarterMiniSerializer
from apps.pedagog.serializers.school import SchoolTypeSerializer
from apps.pedagog.serializers.science import (
    ScienceLanguageSerializer,
    ScienceSerializer,
)


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = [
            "id",
            "school_type",
            "classes",
            "science",
            "science_language",
            "quarter",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user

        plan = Plan.objects.create(**validated_data)
        return plan


class PlanDetailSerializer(serializers.ModelSerializer):
    quarter = QuarterMiniSerializer()
    school_type = SchoolTypeSerializer()
    classes = ClassesSerializer()
    science = ScienceSerializer()
    science_language = ScienceLanguageSerializer()
    is_author = serializers.SerializerMethodField()
    is_topic = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            "id",
            "is_active",
            "is_author",
            "hour",
            "quarter",
            "school_type",
            "classes",
            "science",
            "science_language",
            "is_topic",
            "created_at",
        ]

    def get_is_author(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False

    def get_is_topic(self, obj):
        return Topic.objects.filter(plan_id=obj.id).exists()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            data["is_author"] = instance.user == request.user

        return data


class PlanMiniSerializer(serializers.ModelSerializer):
    quarter = QuarterMiniSerializer()
    classes = ClassesSerializer()
    science = ScienceSerializer()
    science_language = ScienceLanguageSerializer()
    school_type = SchoolTypeSerializer()

    class Meta:
        model = Plan
        fields = [
            "id",
            "quarter",
            "classes",
            "science",
            "science_language",
            "school_type",
        ]


class PlanAdminListSerializer(serializers.ModelSerializer):
    meta = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = [
            "id",
            "name",
            "user",
            "file",
            "type",
            "size",
            "count",
            "meta",
            "created_at",
        ]

    def get_user(self, obj):
        from apps.users.serializers.user import UserSerializer

        user = UserSerializer(obj.user).data
        return {
            "id": user["id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
        }

    def get_meta(self, obj):
        topic = obj.topic.first()
        if topic is None:
            return None

        plan = topic.plan_id
        resource = plan.science.resource_set.first()

        return {
            "plan_id": plan.id,
            "topic": {
                "id": topic.id,
                "name": topic.name,
            },
            "science": {
                "id": plan.science.id,
                "name": plan.science.name,
            },
            "classes": {
                "id": plan.classes.id,
                "name": plan.classes.name,
            },
            "class_type": {
                "id": plan.classes.type.id if plan.classes.type else None,
                "name": plan.classes.type.name if plan.classes.type else None,
            },
            "class_group": {
                "id": plan.class_group.id,
                "name": plan.class_group.name,
            },
            "quarter": {
                "id": plan.quarter.id,
                "name": plan.quarter.name,
            },
            "science_type": {
                "id": plan.science_types.id,
                "name": plan.science_types.name,
            },
            "resource": (
                {
                    "id": resource.id,
                    "name": resource.name,
                }
                if resource
                else None
            ),
            "resource_type": (
                {
                    "id": (resource.type.id if resource and resource.type else None),
                    "name": (
                        resource.type.name if resource and resource.type else None
                    ),
                }
                if resource
                else None
            ),
        }

    def get_size(self, obj):
        size = obj.size

        if size is None:
            return "0 B"

        if size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size / 1024:.2f} KB"
        elif size < 1024**3:
            return f"{size / 1024 ** 2:.2f} MB"
        else:
            return f"{size / 1024 ** 3:.2f} GB"
