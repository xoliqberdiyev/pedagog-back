from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.payment.services.services import get_user_profit, get_user_statistics
from apps.pedagog.models.download import Download
from apps.pedagog.models.media import Media
from apps.pedagog.models.moderator import Moderator
from apps.shared.services.sms import SmsService
from apps.users.models.locations import District, Region
from apps.users.models.user import User
from apps.users.serializers.locations import DistrictSerializer, RegionSerializer


class UserModeratorSerializer(serializers.ModelSerializer):
    _region = RegionSerializer(read_only=True, source="region")
    _district = DistrictSerializer(read_only=True, source="district")

    # Delayed import inside the class
    def __init__(self, *args, **kwargs):
        self.RegionSerializer = RegionSerializer
        self.DistrictSerializer = DistrictSerializer
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["_region"] = self.RegionSerializer(instance.region, read_only=True).data
        ret["_district"] = self.DistrictSerializer(
            instance.district, read_only=True
        ).data
        return ret

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "father_name",
            "phone",
            "password",
            "_region",
            "_district",
            "region",
            "district",
            "institution",
            "institution_number",
        ]

    extra_kwargs = {
        "region": {
            "write_only": True,
        },
        "district": {
            "write_only": True,
        },
    }

    def validate_phone(self, value):
        if User.objects.filter(phone=value, validated_at__isnull=False).exists():
            raise serializers.ValidationError(
                _("Telfon raqam allaqachon ro'yxatdan o'tgan."), code="unique"
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ModeratorCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    father_name = serializers.CharField(source="user.father_name", required=False)
    phone = serializers.CharField(source="user.phone", required=True)
    password = serializers.CharField(
        source="user.password", write_only=True, required=True
    )
    region = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), source="user.region"
    )
    district = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(), source="user.district"
    )
    institution_number = serializers.CharField(source="user.institution_number")
    institution = serializers.CharField(source="user.institution")

    class Meta:
        model = Moderator
        fields = [
            "first_name",
            "last_name",
            "father_name",
            "phone",
            "password",
            "region",
            "district",
            "institution",
            "institution_number",
            "science",
            "science_language",
            "degree",
            "docs",
            "is_contracted",
            "profit",
        ]
        extra_kwargs = {
            "profit": {"read_only": True},
        }

    def create(self, validated_data):
        language = self.context.get("request").headers.get("Accept-Language", "uz")
        user_data = validated_data.pop("user")
        region = user_data.pop("region")
        district = user_data.pop("district")

        user_data["region"] = region.id
        user_data["district"] = district.id

        user_serializer = UserModeratorSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        sms_service = SmsService()
        sms_service.send_confirm(user.phone, language)

        moderator = Moderator.objects.create(user=user, **validated_data)
        return moderator


class ModeratorListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    user_id = serializers.IntegerField(source="user.id")
    phone = serializers.CharField(source="user.phone")
    classes = serializers.StringRelatedField(many=True)
    skachano = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    prosend = serializers.IntegerField()
    card_number = serializers.SerializerMethodField()

    def get_card_number(self, obj):
        card_number = obj.card_number
        if card_number:
            formatted_card_number = "{} **** **** {}".format(
                card_number[:4], card_number[4:8], card_number[8:]
            )
            return formatted_card_number
        return None

    def get_balance(self, obj):
        user_profit = get_user_profit(obj.user)
        return user_profit

    class Meta:
        model = Moderator
        fields = [
            "id",
            "user_id",
            "first_name",
            "last_name",
            "classes",
            "phone",
            "card_number",
            "skachano",
            "prosend",
            "balance",
            "is_contracted",
        ]

    def get_skachano(self, obj):
        user_downloads = Download.objects.filter(user=obj.user)
        return user_downloads.count()


class ModeratorDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    user_id = serializers.IntegerField(source="user.id")
    phone = serializers.CharField(source="user.phone")
    avatar = serializers.ImageField(source="user.avatar")
    region = serializers.StringRelatedField(source="user.region")
    district = serializers.StringRelatedField(source="user.district")
    father_name = serializers.StringRelatedField(source="user.father_name")
    institution = serializers.StringRelatedField(source="user.institution")
    role = serializers.StringRelatedField(source="user.role")
    school_type = serializers.StringRelatedField(many=True)
    classes = serializers.StringRelatedField(many=True)
    science = serializers.StringRelatedField(many=True)
    science_language = serializers.StringRelatedField(many=True)
    resource_type = serializers.StringRelatedField(many=True)
    status = serializers.BooleanField(source="is_contracted")
    balance = serializers.SerializerMethodField()
    downloads_count = serializers.SerializerMethodField()
    media_count = serializers.SerializerMethodField()
    resources_count = serializers.SerializerMethodField()
    card_number = serializers.SerializerMethodField()

    def get_balance(self, obj):
        user_profit = get_user_profit(obj.user)
        return user_profit

    def get_media_count(self, obj):
        medias = obj.user.media.all()
        return medias.count()

    def get_downloads_count(self, obj):
        downloads_count, _ = get_user_statistics(obj.user)
        return downloads_count

    def get_resources_count(self, obj):
        _, resource_count = get_user_statistics(obj.user)
        return resource_count

    def get_card_number(self, obj):
        card_number = obj.card_number
        if card_number:
            formatted_card_number = "{} **** **** {}".format(
                card_number[:4], card_number[12:]
            )
            return formatted_card_number
        return None

    class Meta:
        model = Moderator
        fields = [
            "id",
            "user_id",
            "first_name",
            "last_name",
            "classes",
            "phone",
            "avatar",
            "region",
            "district",
            "father_name",
            "institution",
            "role",
            "card_number",
            "is_contracted",
            "status",
            "balance",
            "media_count",
            "downloads_count",
            "resources_count",
            "school_type",
            "science",
            "science_language",
            "resource_type",
        ]


class SendMoneySerializer(serializers.Serializer):
    moderator_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True, min_length=1
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class ModeratorTemetikPlanSerializer(serializers.ModelSerializer):
    meta = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = [
            "id",
            "name",
            "profit",
            "file",
            "type",
            "size",
            "count",
            "statistics",
            "object_type",
            "object_id",
            "meta",
            "created_at",
        ]

    def get_profit(self, obj):
        return get_user_profit(obj.user)

    def get_meta(self, obj):
        topic = obj.topic.first()
        if topic is None:
            return None
        plan = topic.plan_id
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
            "quarter": {
                "id": plan.quarter.id,
                "name": plan.quarter.name,
            },
            "science_type": {
                "id": plan.science_types.id,
                "name": plan.science_types.name,
            },
            "class_group": {
                "id": plan.class_group.id,
                "name": plan.class_group.name,
            },
        }
