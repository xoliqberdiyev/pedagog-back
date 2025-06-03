from rest_framework import serializers

from apps.pedagog.models.quarter import Quarter


class QuarterMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarter
        fields = ("id", "choices", "start_date", "end_date")
