from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from apps.users.models.user import SourceChoice
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models.locations import Region, District
from apps.users.models.user import User


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": _(
            "Berilgan hisob maʼlumotlari bilan faol hisob topilmadi."
        )
    }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    father_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    region = serializers.CharField(max_length=255)
    district = serializers.CharField(max_length=255)
    institution_number = serializers.CharField(max_length=255, required=False)
    source = serializers.ChoiceField(choices=SourceChoice.choices, required=False)

    def validate_phone(self, value):
        user = User.objects.filter(phone=value)
        if user.exists():
            raise exceptions.ValidationError(
                _("Phone number already registered."), code="unique"
            )
        return value

    def validate(self, attrs):
        if not attrs.get("region") or not attrs.get("district"):
            raise exceptions.ValidationError(
                _("Region and district are required."), code="invalid"
            )
        return attrs

    def validate_region(self, value):
        if not Region.objects.filter(id=value).exists():
            raise exceptions.ValidationError(
                _("Region does not exist."), code="invalid"
            )
        return value

    def validate_district(self, value):
        if not District.objects.filter(id=value).exists():
            raise exceptions.ValidationError(
                _("District does not exist."), code="invalid"
            )
        return value


class ModeratorRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    father_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    region = serializers.CharField(max_length=255)
    district = serializers.CharField(max_length=255)
    institution_number = serializers.CharField(max_length=255, required=False)
    degree = serializers.CharField(max_length=255, required=False)
    docs = serializers.ListField(child=serializers.FileField(), required=False)
    role = serializers.CharField(max_length=50, default="moderator", required=False)
    source = serializers.ChoiceField(choices=SourceChoice.choices, required=False)
    

    def validate_phone(self, value):
        user = User.objects.filter(phone=value)
        if user.exists():
            raise exceptions.ValidationError(
                _("Phone number already registered."), code="unique"
            )
        return value

    def validate(self, attrs):
        if not attrs.get("region") or not attrs.get("district"):
            raise exceptions.ValidationError(
                _("Region and district are required."), code="invalid"
            )
        return attrs

    def validate_region(self, value):
        if not Region.objects.filter(id=value).exists():
            raise exceptions.ValidationError(
                _("Region does not exist."), code="invalid"
            )
        return value

    def validate_district(self, value):
        if not District.objects.filter(id=value).exists():
            raise exceptions.ValidationError(
                _("District does not exist."), code="invalid"
            )
        return value


class ConfirmSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=1000, max_value=9999)
    phone = serializers.CharField(max_length=255)


class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)

    def validate_phone(self, value):
        user = User.objects.filter(phone=value)
        if user.exists():
            return value

        raise serializers.ValidationError(_("Foydalanuvchi topilmadi"))


class ResetConfirmationSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=1000, max_value=9999)
    phone = serializers.CharField(max_length=255)

    def validate_phone(self, value):
        user = User.objects.filter(phone=value)
        if user.exists():
            return value
        raise serializers.ValidationError(_("User does not exist"))


class ResendSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)
