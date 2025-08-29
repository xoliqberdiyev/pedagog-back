from django.conf import settings
from rest_framework import serializers

from apps.pedagog.models.moderator import Moderator
from apps.users.choices.role import Role
from apps.users.models.user import User, BotUsers


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None)
    resource_creatable = serializers.SerializerMethodField(read_only=True)
    plan_creatable = serializers.SerializerMethodField(read_only=True)
    topic_creatable = serializers.SerializerMethodField(read_only=True)
    is_contracted = serializers.SerializerMethodField(read_only=True)
    
    referral_count = serializers.SerializerMethodField()


    class Meta:
        fields = [
            "id",
            "avatar",
            "first_name",
            "last_name",
            "father_name",
            "phone",
            "role",
            "region",
            "tg_id",
            "referral_code",
            "referral_count",
            
            "district",
            "institution_number",
            "resource_creatable",
            "plan_creatable",
            "topic_creatable",
            "is_contracted",
        ]
        extra_kwargs = {
            "role": {"read_only": True},
            "resource_creatable": {"read_only": True},
            "plan_creatable": {"read_only": True},
        }
        model = User

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url.replace(settings.MEDIA_URL, "/media/")
        return None
    
    def get_referral_count(self, obj):
        return obj.referrals.count()

    def is_moderator(self, obj):
        return obj.role == Role.MODERATOR or obj.role == Role.ADMIN

    def get_is_contracted(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.is_contracted
            except Moderator.DoesNotExist:
                return False
        return False

    def get_resource_creatable(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.resource_creatable
            except Moderator.DoesNotExist:
                return False
        return False

    def get_plan_creatable(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.plan_creatable
            except Moderator.DoesNotExist:
                return False
        return False

    def get_topic_creatable(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.topic_creatable
            except Moderator.DoesNotExist:
                return False
        return False

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.father_name = validated_data.get("father_name", instance.father_name)
        instance.region = validated_data.get("region", instance.region)
        instance.district = validated_data.get("district", instance.district)
        instance.institution_number = validated_data.get(
            "institution_number", instance.institution_number
        )
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request and request.user.role == Role.USER:
            data.pop("is_contracted", None)
        return data


class UserRoleChangeSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Role)

    class Meta:
        model = User
        fields = ["role"]


class UserDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None)
    resource_creatable = serializers.SerializerMethodField(read_only=True)
    plan_creatable = serializers.SerializerMethodField(read_only=True)
    topic_creatable = serializers.SerializerMethodField(read_only=True)
    is_contracted = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = [
            "id",
            "avatar",
            "first_name",
            "last_name",
            "father_name",
            "phone",
            "role",
            "region",
            "district",
            "institution_number",
            "resource_creatable",
            "plan_creatable",
            "topic_creatable",
            "is_contracted",
        ]
        extra_kwargs = {
            "role": {"read_only": True},
            "resource_creatable": {"read_only": True},
            "plan_creatable": {"read_only": True},
        }
        model = User

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url.replace(settings.MEDIA_URL, "/media/")
        return None

    def is_moderator(self, obj):
        return obj.role == Role.MODERATOR or obj.role == Role.ADMIN

    def get_is_contracted(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.is_contracted
            except Moderator.DoesNotExist:
                return False
        return False

    def get_resource_creatable(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.resource_creatable
            except Moderator.DoesNotExist:
                return False
        return False

    def get_plan_creatable(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.plan_creatable
            except Moderator.DoesNotExist:
                return False
        return False

    def get_topic_creatable(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.topic_creatable
            except Moderator.DoesNotExist:
                return False
        return False

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request and request.user.role == Role.USER:
            data.pop("is_contracted", None)

        return data


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "avatar", "first_name", "last_name"]
        model = User


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "avatar",
            "first_name",
            "last_name",
            "father_name",
            "region",
            "district",
            "institution_number",
        ]
        model = User


    
class BotUsersSerialiers(serializers.ModelSerializer):
    class Meta:
        model = BotUsers
        fields = [
            "id",
            "tg_id",
            "first_name"
        ]