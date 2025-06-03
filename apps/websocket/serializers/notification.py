from rest_framework import serializers

from apps.websocket.models.notification import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "user", "message", "is_read", "created_at"]
        read_only_fields = ["id", "created_at"]
