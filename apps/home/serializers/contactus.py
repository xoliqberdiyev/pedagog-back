from rest_framework import serializers

from apps.home.models.contactus import ContactUs


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ["id", "first_name", "last_name", "phone", "text", "created_at"]
        read_only_fields = ["id", "created_at"]
