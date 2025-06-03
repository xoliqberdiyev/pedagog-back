from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.home.serializers.contactus import ContactUsSerializer


class ContactUsView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ContactUsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Contact us message sent successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": "Failed to send contact us message.",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
