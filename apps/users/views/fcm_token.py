from rest_framework import views, permissions
from rest_framework.response import Response

from apps.users.models.notification import FCMToken


class FCMTokenApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'success': False, 'message': 'Token kiritilmagan'}, status=400)

        user = request.user
        FCMToken.objects.get_or_create(
            user=user,
            token=token
        )
        return Response({'success': True, 'message': 'Token saqlandi'}, status=200)
