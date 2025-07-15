from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.moderator.models.permission import ModeratorPermission
from apps.moderator.serializers.permission import ModeratorPermissionSerializer
from apps.shared.pagination.custom import CustomPagination
from apps.moderator.filters import ModeratorPermissionFilter


class ModeratorPermissionView(APIView):
    """
    API view to handle moderator permissions.
    """

    serializer_class = ModeratorPermissionSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Returns the queryset for the moderator permissions.
        """
        return ModeratorPermission.objects.filter(user=self.request.user)

    def get(self, request):
        """
        List all moderator permissions.
        """
        queryset = ModeratorPermissionFilter(request.GET, queryset=self.get_queryset()).qs

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new moderator permission.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
