from rest_framework import serializers

from apps.pedagog.models.degree import Degree


class DegreeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Degree model.
    """

    class Meta:
        model = Degree
        fields = ("id", "name", "created_at")
