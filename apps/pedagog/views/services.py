from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from apps.pedagog.models.services import ServicesModel
from apps.pedagog.serializers.services import ServicesSerializer
from apps.shared.pagination.custom import CustomPagination


class ServicesViewset(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = ServicesModel.objects.order_by("-id").all()
    serializer_class = ServicesSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]
