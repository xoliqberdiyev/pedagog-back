from rest_framework import serializers

from apps.home.models.info import PedagogInfo


class PedagogInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for PedagogInfo model.
    """

    class Meta:
        model = PedagogInfo
        fields = (
            "id",
            "title",
            "description",
            "image",
            "icon",
            "created_at",
        )
