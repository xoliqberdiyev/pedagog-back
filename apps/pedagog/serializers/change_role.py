from django.utils.translation import gettext_lazy as _  # noqa
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from apps.pedagog.models.documents import Document
from apps.pedagog.models.moderator import Moderator
from apps.shared.utils.logger import logger


class ChangeRoleSerializer(serializers.ModelSerializer):
    docs = serializers.ListField(child=serializers.FileField(), write_only=True)

    class Meta:
        model = Moderator
        fields = [
            "degree",
            "docs",
        ]

    def create(self, data):
        try:
            request = self.context.get("request")
            user = request.user
            docs_data = []

            for key in request.data:
                if key.startswith("description[") and key.endswith("]"):
                    index = key[len("description[") : -1]  # noqa: E203
                    file_key = f"docs[{index}]"
                    doc_desc = request.data.get(key)
                    doc_file = request.FILES.get(file_key)

                    if not doc_file:
                        return Response(
                            {"error": f"File is required for document item {index}"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    if not doc_desc:
                        doc_desc = doc_file.name
                    docs_data.append({"docs": doc_file, "description": doc_desc})

            moderator, created = Moderator.objects.update_or_create(
                user=user, defaults={"degree": data.get("degree")}
            )

            for doc_data in docs_data:
                document = Document.objects.create(
                    file=doc_data["docs"], description=doc_data["description"]
                )
                moderator.docs.add(document)

            return moderator
        except Exception as e:
            logger.error(f"Error in create method: {str(e)}")
            raise exceptions.ValidationError({"detail": str(e)})
