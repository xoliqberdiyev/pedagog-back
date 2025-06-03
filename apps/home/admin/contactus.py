from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.home.models.contactus import ContactUs


@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin):
    list_display = ["first_name", "last_name", "phone", "text", "created_at"]
    search_fields = ["first_name", "last_name", "phone", "text"]
    list_filter = ["created_at"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    list_per_page = 20
