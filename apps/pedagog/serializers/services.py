from rest_framework import serializers

from apps.pedagog.models.services import ServicesModel


class ServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServicesModel
        fields = [
            "id",
            "logo",
            "title",
            "url",
        ]
