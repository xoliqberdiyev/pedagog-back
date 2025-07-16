from rest_framework import serializers

from apps.pedagog.models.documents import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            "id",
            "user",
            "title",
            "description",
            "file",
            "passport_file",
            "document_file",
            "type",
            "size",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
