from django.db import models 

from apps.shared.models.base import AbstractBaseModel
from apps.users.models.user import User


class FCMToken(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fcm_tokens')
    token = models.CharField(max_length=250)

    class Meta:
        unique_together = ('user', 'token')
    