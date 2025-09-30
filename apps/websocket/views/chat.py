from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.choices.role import Role
from apps.websocket.chatconsumer import User
from apps.websocket.models.chat import ChatRoom, Message
from apps.websocket.serializers.chat import (
    ChatRoomSerializer,
    MessageSerializer,
    WsMessageSerializer,
)


class ChatRoomList(APIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        search_term = request.GET.get("search", None)

        if user.role == Role.ADMIN:
            chat_rooms = ChatRoom.objects.all()
            for chat_room in chat_rooms:
                if not chat_room.participants.filter(id=user.id).exists():
                    chat_room.participants.add(user)
        else:
            chat_rooms = ChatRoom.objects.filter(participants=user, messages__isnull=False).distinct()
            admins = User.objects.filter(role=Role.ADMIN)

            if not chat_rooms.exists():
                first_name = user.first_name if user.first_name else "Ism"
                last_name = user.last_name if user.last_name else "Familiya"
                father_name = user.father_name if user.father_name else "Otasining ismi"
                phone = user.phone if user.phone else user.email
                chat_room = ChatRoom.objects.create(
                    name=f"{first_name} {last_name} {father_name} - {phone}"
                )
                chat_room.participants.add(user)
                chat_rooms = [chat_room]
                for admin in admins:
                    chat_room.participants.add(admin)

        # Qidiruvni amalga oshirish
        if search_term:
            chat_rooms = chat_rooms.filter(
                name__icontains=search_term
            )  # `name` bo'yicha qidiruv

        serializer = self.serializer_class(chat_rooms, many=True)
        return Response(
            {
                "success": True,
                "message": "Chat rooms fetched successfully.",
                "data": serializer.data,
            }
        )


class MessageList(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        if pk is None:
            raise MethodNotAllowed("GET method not allowed")
        messages = Message.objects.filter(chat_id=pk)
        serializer = self.serializer_class(messages, many=True, context={"rq": request})
        return Response(
            {
                "success": True,
                "message": "Messages fetched successfully.",
                "data": serializer.data,
            }
        )

    def _send_ws_message(self, group, data):
        # Send message to group
        async_to_sync(get_channel_layer().group_send)(
            group,
            {
                "type": "chat_message",
                **data,
            },
        )

    def post(self, request, format=None):
        user = request.user
        chat_id = request.data.get("chat_id")
        message = request.data.get("message")
        file = request.data.get("file")

        if not chat_id:
            return Response({"success": False, "message": "Chat ID is required"})

        try:
            chats = ChatRoom.objects.get(id=chat_id)
        except ChatRoom.DoesNotExist:
            return Response({"success": False, "message": "Chat not found"})
        message = Message.objects.create(
            chat=chats, sender=user, message=message, file=file
        )
        serializer = self.serializer_class(message)
        self._send_ws_message(
            f"chat_{chat_id}", WsMessageSerializer(instance=message).data
        )
        return Response(
            {
                "success": True,
                "message": "Message created successfully.",
                "data": serializer.data,
            }
        )


class ModeratorMessageUpdate(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, format=None):
        user = request.user
        message = get_object_or_404(Message, pk=pk)

        if user.role == Role.ADMIN:
            serializer = self.serializer_class(
                message,
                data=request.data,
                partial=True,
                context={"rq": request},
            )
            if serializer.is_valid():
                serializer.save()
                message.chat.message_count = 0
                Message.objects.filter(chat=message.chat).update(is_read=True)
                message.chat.save()
                return Response(
                    {
                        "success": True,
                        "message": "Message updated successfully.",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Message could not be updated.",
                        "data": serializer.errors,
                    },
                    status=400,
                )
        elif user.role == Role.USER or user.role == Role.MODERATOR:
            serializer = self.serializer_class(
                message,
                data=request.data,
                partial=True,
                context={"rq": request},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "Message updated successfully.",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Message could not be updated.",
                        "data": serializer.errors,
                    },
                    status=400,
                )
        else:
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to update this message.",
                    "data": [],
                },
                status=403,
            )

    def delete(self, request, pk, format=None):
        user = request.user
        message = get_object_or_404(Message, pk=pk, sender=user)
        message.delete()
        return Response(
            {
                "success": True,
                "message": "Message deleted successfully.",
                "data": [],
            }
        )


class CreateChatRoomApiViews(APIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        message_data = request.data.get("message")

        if user.role == "admin":
            return Response(
                {"success": False, "message": "foydalanuvchi emas!"},
                status=400,
            )

        admins = User.objects.filter(role="admin")

        chat_rooms, created = ChatRoom.objects.get_or_create(name=f"{user.username}")

        chat_rooms.participants.add(user)

        chat_rooms.participants.add(*admins)

        message = Message.objects.create(
            chat=chat_rooms, sender=user, message=message_data
        )
        chat_rooms.last_message = message
        chat_rooms.message_count += 1
        chat_rooms.save()

        serializer = ChatRoomSerializer(chat_rooms, context={"request": self.request})

        return Response(
            {
                "success": True,
                "message": "Chat xonasi yaratildi va xabar yuborildi.",
                "data": serializer.data,
            }
        )
