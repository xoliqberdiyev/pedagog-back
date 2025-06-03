from rest_framework import serializers

from apps.pedagog.models.moderator import Moderator
from apps.users.serializers.locations import RegionSerializer, DistrictSerializer
from apps.users.models.user import User


class UserAdminSiteSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    district = DistrictSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "father_name",
            "avatar",
            "phone",
            "region",
            "district",
            "institution_number",
        ]


class ModeratorAdminSiteSerializer(serializers.ModelSerializer):
    user = UserAdminSiteSerializer()

    class Meta:
        model = Moderator
        fields = (
            "id",
            "user",
            "balance",
            "degree",
            "is_contracted",
            "status",
            "profit",
        )
        read_only_fields = ("user",)
