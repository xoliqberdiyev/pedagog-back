from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.moderator.serializers.permission import ModeratorPermissionSerializer


class ModeratorPermissionView(APIView):
    """
    API view to handle moderator permissions.
    """

    serializer_class = ModeratorPermissionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Create a new moderator permission.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
