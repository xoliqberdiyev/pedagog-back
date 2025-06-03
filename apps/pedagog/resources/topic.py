from import_export import resources

from apps.pedagog.models.topic import Topic


class TopicResource(resources.ModelResource):
    class Meta:
        model = Topic
        fields = (
            "id",
            "sequence_number",
            "weeks",
            "name",
            "description",
            "hours",
            "plan_id",
        )
