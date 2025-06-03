from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from apps.home.models.blog import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
            )
        }
