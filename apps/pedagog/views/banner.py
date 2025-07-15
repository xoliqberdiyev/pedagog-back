from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from apps.pedagog.models.banner import BannerModel
from apps.pedagog.serializers.banner import BannerSerializer
from apps.shared.pagination.custom import CustomPagination


class BannerViewset(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = BannerSerializer
    queryset = BannerModel.objects.order_by("-id").all()
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
