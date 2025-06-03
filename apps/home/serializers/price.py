from rest_framework import serializers

from apps.payment.models.models import PlansRequirements, Plans
from apps.pedagog.serializers.quarter import QuarterMiniSerializer


class PlansRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlansRequirements
        fields = ("id", "name")
        read_only_fields = ("id",)


class PriceSerializer(serializers.ModelSerializer):
    quarter = QuarterMiniSerializer(read_only=True)

    class Meta:
        model = Plans
        fields = (
            "id",
            "price",
            "title",
            "description",
            "icon",
            "quarter",
        )
        read_only_fields = ("id",)

    def to_representation(self, instance):
        """
        Customize the representation of the serializer.
        """
        data = super().to_representation(instance)
        data["requirements"] = PlansRequirementsSerializer(
            instance.requirements.all(), many=True
        ).data
        return data
