from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from apps.pedagog.models.video import VideoModel
from apps.pedagog.serializers.video import VideoSerializer
from apps.shared.pagination.custom import CustomPagination


class VideoViewset(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = VideoSerializer
    queryset = VideoModel.objects.order_by("-id").all()
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
