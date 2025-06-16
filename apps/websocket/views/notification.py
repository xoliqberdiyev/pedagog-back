from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.views.locations import CustomPagination
from apps.websocket.models.notification import Notification
from apps.websocket.serializers.notification import NotificationSerializer


class NotificationApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class NotificationDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def patch(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        serializer = self.serializer_class(
            notification, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
