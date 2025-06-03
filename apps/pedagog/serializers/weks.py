from rest_framework import serializers

from apps.pedagog.models.weeks import Weeks
from apps.pedagog.serializers.quarter import QuarterMiniSerializer


class WeeksSerializer(serializers.ModelSerializer):
    quarter = QuarterMiniSerializer()

    class Meta:
        model = Weeks
        fields = [
            "id",
            "quarter",
            "week_count",
            "start_date",
            "end_date",
            "created_at",
        ]
