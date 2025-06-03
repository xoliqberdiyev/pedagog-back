import typing
from datetime import datetime

from django.utils import translation
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt import tokens

from apps.users.choices.role import Role
from apps.shared.exceptions.core import SmsException
from apps.shared.services.sms import SmsService
from apps.users.models.locations import Region, District
from apps.users.models.user import User


class UserService(SmsService):
    def get_token(self, user):
        refresh = tokens.RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def create_user(
        self,
        phone,
        first_name,
        last_name,
        father_name,
        password,
        region_id,
        district_id,
        institution_number,
        role=Role.USER,
    ):
        region = get_object_or_404(Region, id=region_id)
        district = get_object_or_404(District, id=district_id)
        print(role)

        user, _ = User.objects.update_or_create(
            phone=phone,
            defaults={
                "phone": phone,
                "first_name": first_name,
                "last_name": last_name,
                "father_name": father_name,
                "role": role,
                "region": region,
                "district": district,
                "institution_number": institution_number,
            },
        )
        user.set_password(password)
        user.save()
        return user

    def send_confirmation(self, phone, language):
        translation.activate(language)
        try:
            self.send_confirm(phone, language)
            return True
        except SmsException as e:
            ResponseException(e, data={"expired": e.kwargs.get("expired")})  # noqa
        except Exception as e:
            ResponseException(e)  # noqa

    def validate_user(self, user: typing.Union[User]) -> dict:
        """
        Create user if user not found
        """
        user.validated_at = datetime.now()
        user.save()
        token = self.get_token(user)
        return token

    def is_validated(self, user: typing.Union[User]) -> bool:
        """
        User is validated check
        """
        if user.validated_at is not None:
            return True
        return False

    def change_password(self, phone, password):
        """
        Change password
        """
        user = User.objects.filter(phone=phone).first()
        user.set_password(password)
        user.save()
