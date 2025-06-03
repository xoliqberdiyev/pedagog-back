from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from apps.home.models.privacy import PrivacyPolicy


class PrivacyPolicyForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy
        fields = "__all__"
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
            )
        }
