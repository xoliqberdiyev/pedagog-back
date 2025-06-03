from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from apps.home.models.news import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
            )
        }
