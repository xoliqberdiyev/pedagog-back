from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.home.serializers.price import PriceSerializer
from apps.payment.models.models import Plans
from apps.shared.pagination.custom import PedagogPagination


class PriceView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PriceSerializer
    queryset = Plans.objects.all()
    pagination_class = PedagogPagination

    def get(self, request):
        """
        Handle GET requests to retrieve a list of price.
        """
        queryset = self.queryset
        paginator = self.pagination_class()
        paginated_categories = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_categories, many=True)
        return paginator.get_paginated_response(serializer.data)
