from import_export import resources

from apps.pedagog.models.topic import Topic


class TopicResource(resources.ModelResource):
    class Meta:
        model = Topic
        fields = (
            "id",
            "plan_id",
            "name",
            "description",
            "sequence_number",
            "hours",
            "weeks",
        )
