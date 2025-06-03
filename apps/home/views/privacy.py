from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.home.models.privacy import PrivacyPolicy
from apps.home.serializers.privacy import PrivacyPolicySerializer
from apps.shared.pagination.custom import PedagogPagination


class PrivacyPolicyView(APIView):
    """
    API view to retrieve the privacy policy.
    """

    permission_classes = [AllowAny]
    serializer_class = PrivacyPolicySerializer
    queryset = PrivacyPolicy.objects.all()
    pagination_class = PedagogPagination

    def get(self, request):
        """
        Handle GET requests to retrieve a list of blog categories.
        """
        queryset = self.queryset
        paginator = self.pagination_class()
        paginated_categories = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_categories, many=True)
        return paginator.get_paginated_response(serializer.data)
