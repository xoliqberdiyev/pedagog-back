from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.pedagog.models.moderator import Moderator
from apps.users.serializers.user import UserSerializer
from apps.users.models.user import User
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number_field = "phone"
    
    def validate(self, attrs):
        phone = attrs.get(self.phone_number_field)
        password = attrs.get("password")

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "Bu telefon raqami bilan ro'yxatdan o'tilmagan"}
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                {"detail": "Parol noto'g'ri"}
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                {"detail": "Bu akkaunt faol emas"}
            )

        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        # Check if the user is a moderator
        # if self.user.role == "moderator":
        #     try:
        #         moderator = Moderator.objects.get(user=self.user)
        #         data["user"]["is_contracted"] = moderator.is_contracted
        #     except Moderator.DoesNotExist:
        #         data["user"]["is_contracted"] = False
        # else:
        #     data["user"].pop("is_contracted", None)
        #
        return data
