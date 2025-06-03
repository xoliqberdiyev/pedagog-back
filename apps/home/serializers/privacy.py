from rest_framework import serializers

from apps.home.models.privacy import PrivacyPolicy


class PrivacyPolicySerializer(serializers.ModelSerializer):
    """
    Serializer for the PrivacyPolicy model.
    """

    class Meta:
        model = PrivacyPolicy
        fields = (
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")
