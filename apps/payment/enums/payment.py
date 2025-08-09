from django.db import models
from django.utils.translation import gettext_lazy as _

class PaymentType(models.TextChoices):
    click = "click", _("Click")
    payme = "payme", _("Payme")
    uzum = "uzum", _("Uzum")