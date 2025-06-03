from django.utils.translation import gettext_lazy as _
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.pedagog.models.moderator import Moderator
from apps.pedagog.serializers.change_role import ChangeRoleSerializer


class ChangeRoleView(generics.CreateAPIView):
    queryset = Moderator.objects.all()
    serializer_class = ChangeRoleSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if Moderator.objects.filter(user=user).exists():
            return Response(
                {"detail": _("Siz ariza topshirgansiz")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
