from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.decorators import display

from apps.pedagog.models.topic import Topic
from apps.pedagog.resources.topic import TopicResource


@admin.register(Topic)
class TopicAdmin(ModelAdmin, ImportExportModelAdmin):
    """Topic admin

    Args:
        ImportExportModelAdmin (_type_): _description_
    """

    resource_class = TopicResource
    list_filter_submit = True
    list_display = (
        "id",
        "sequence_number",
        "name",
        "description",
        "hours",
        "weeks",
        "plan_id",
        "downloads_count",
    )
    search_fields = (
        "name",
        "description",
    )
    autocomplete_fields = (
        "plan_id",
        "user",
    )

    @display(label=True)
    def downloads_count():
        return 0
