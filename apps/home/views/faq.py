from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.home.models.faq import FAQ
from apps.home.serializers.faq import FAQSerializer


class FAQList(APIView):
    permission_classes = [AllowAny]
    serializer_class = FAQSerializer

    def get_queryset(self):
        return FAQ.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class FAQDetail(APIView):
    permission_classes = [AllowAny]
    serializer_class = FAQSerializer

    def get(self, request, pk):
        queryset = get_object_or_404(FAQ, pk=pk)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)
