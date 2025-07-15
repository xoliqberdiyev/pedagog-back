from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.pedagog.models.services import ServicesModel


@admin.register(ServicesModel)
class ServicesAdmin(ModelAdmin):
    list_display = [
        "id",
        "title",
        "url",
    ]
