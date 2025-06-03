from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

    def validate(self, data):
        if self.context.get("request").user is None:
            raise serializers.ValidationError(
                {
                    "detail": _(
                        "Foydalanuvchi topilmadi. Iltimos, qayta  urinib ko'ring."
                    ),
                }
            )
        return data
