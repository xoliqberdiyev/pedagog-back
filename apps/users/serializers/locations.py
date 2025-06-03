from rest_framework import serializers

from apps.users.models.locations import District
from apps.users.models.locations import Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name", "soato_id"]
        ordering = ["region"]


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ["id", "name", "soato_id"]
