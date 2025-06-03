from rest_framework import serializers

from apps.pedagog.models.documents import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
