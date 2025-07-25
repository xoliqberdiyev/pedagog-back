from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.pedagog.serializers.media_type import MediaTypeSerializer
from apps.pedagog.models.media_type import MediaType


class MediaTypeListApiView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        media_type = MediaType.objects.all()
        serializer = MediaTypeSerializer(media_type, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)