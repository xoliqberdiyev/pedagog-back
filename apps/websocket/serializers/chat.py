from rest_framework import serializers


from django.contrib.auth import get_user_model

from apps.websocket.models.chat import Message, ChatRoom


class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "father_name",
            "phone",
            "role",
        ]


class MessageLastSerializer(serializers.ModelSerializer):
    sender = SenderSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "chat",
            "sender",
            "message",
            "is_read",
            "created_at",
            "updated_at",
        )


class ChatRoomSerializer(serializers.ModelSerializer):
    last_message = MessageLastSerializer(read_only=True)
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj) -> str:
        request = self.context.get("request", None)
        if request is None:
            return None
        user_id = request.user.id
        user = obj.participants.exclude(id=user_id).first()
        if user is None:
            return None
        return user.avatar

    class Meta:
        model = ChatRoom
        fields = (
            "id",
            "name",
            "avatar",
            "message_count",
            "last_message",
            "created_at",
            "updated_at",
        )


class ChatMiniRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatRoom
        fields = (
            "id",
            "name",
        )


class MessageSerializer(serializers.ModelSerializer):
    chat = ChatMiniRoomSerializer(read_only=True)
    sender = SenderSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "chat",
            "sender",
            "message",
            "is_read",
            "is_read",
            "created_at",
            "updated_at",
        )


class WsMessageSerializer(serializers.ModelSerializer):
    chat = ChatMiniRoomSerializer(read_only=True)
    sender = SenderSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "chat",
            "sender",
            "message",
            "is_read",
            "is_read",
            "created_at",
            "updated_at",
        )


class CallSerializer(serializers.Serializer):
    ACTIONS = [
        ("call", "call"),
    ]
    chat = serializers.IntegerField(required=True)
    action = serializers.ChoiceField(choices=ACTIONS)
    data = serializers.JSONField(required=False, default={})
