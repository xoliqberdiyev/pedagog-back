from rest_framework import serializers


from apps.users.models.user import UserProfile
from apps.users.serializers.document import DocumentSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "document",
            "response_file",
            "status_file",
            "status",
            "balance",
            "card_number",
        )
        read_only_fields = ("id", "user")

    def to_representation(self, instance):
        """
        Customize the representation of the UserProfile to include user details.
        """
        representation = super().to_representation(instance)
        representation["document"] = DocumentSerializer(
            instance.document, many=True
        ).data
        return representation
