from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pedagog.models.quarter import Quarter
from apps.pedagog.models.weeks import Weeks
from apps.pedagog.serializers.weks import WeeksSerializer


class WeeksByQuarterView(APIView):
    def get(self, request):
        quarter_id = request.query_params.get("quarter_id")

        if quarter_id:
            try:
                quarter = Quarter.objects.get(id=quarter_id)
            except Quarter.DoesNotExist:
                return Response(
                    {"error": "Quarter not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            weeks = Weeks.objects.filter(quarter=quarter)
        else:
            weeks = Weeks.objects.all()

        serializer = WeeksSerializer(weeks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
