from rest_framework import serializers

from apps.pedagog.models.documents import Document, FileModel


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileModel
        fields = [
            "id",
            "file",
        ]


class DocumentSerializer(serializers.ModelSerializer):
    passport_file = serializers.ListField(
        child=serializers.FileField(
            max_length=100000, allow_empty_file=False, use_url=False
        ),
        allow_empty=False,
        write_only=True,
    )

    document_file = serializers.ListField(
        child=serializers.FileField(
            max_length=100000, allow_empty_file=False, use_url=False
        ),
        allow_empty=False,
        write_only=True,
    )

    def create(self, validated_data):
        passport_files = validated_data.pop("passport_file")
        document_files = validated_data.pop("document_file")
        document = Document.objects.create(**validated_data)

        for file in passport_files:
            document.passport_file.add(FileModel.objects.create(file=file))

        for file in document_files:
            document.document_file.add(FileModel.objects.create(file=file))
        return document

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["passport_file"] = FileSerializer(
            instance.passport_file.all(), many=True, context=self.context
        ).data
        data["document_file"] = FileSerializer(
            instance.document_file.all(), many=True, context=self.context
        ).data
        return data

    class Meta:
        model = Document
        fields = (
            "id",
            "user",
            "title",
            "description",
            # "file",
            "passport_file",
            "document_file",
            "type",
            "size",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
