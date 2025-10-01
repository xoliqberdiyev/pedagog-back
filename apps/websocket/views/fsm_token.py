from rest_framework import views, permissions
from rest_framework.response import Response

from apps.websocket.models.notification import FSMToken


class FSMTokenApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        token = request.data.get('token')
        if not token:
            return Response(
                {
                    'success': False,
                    'message': 'token is required'
                }, status=400
            )
        fsm_token, created = FSMToken.objects.get_or_create(
            user=user, token=token
        )
        if created:
            return Response(
                {
                    'success': True,
                    'message': 'Token saved',
                }, status=200
            )
        return Response(
            {
                'success': True,
                'message': 'Token exists',
            }, status=200
        )
