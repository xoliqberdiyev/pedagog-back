import requests, logging

from django.conf import settings

from rest_framework import views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from click_up.views import ClickWebhook

from apps.payment.models.models import Orders, Payments
from apps.users.models.user import User

logger = logging.getLogger(__name__)


class ClickWebhookAPIView(ClickWebhook):
    def successfully_payment(self, params):
        """
        successfully payment method process you can ovveride it
        """
        print(f"payment successful params: \n\n\n\n{params}\n\n\n")
        
         
        try:
            merchant_trans_id = params.merchant_trans_id

            
            payment = Payments.objects.filter(trans_id=merchant_trans_id).first()
            order = payment.order

            order.status = True
            order.save()

            payment.status = True
            payment.save()


        except Exception as e:
            print(f"===========\n\n{e}\n\n========================")

    def cancelled_payment(self, params):
        """
        cancelled payment method process you can ovveride it
        """
        print(f"payment cancelled params: {params}")

    
class ClickProfileView(views.APIView):
    def get(self, request):
        web_session = request.headers.get('web_session')
        print("Headers:", dict(request.headers))
        
        if not web_session:
            return Response(
                {
                    'error': 'web_session not found',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {settings.CLICK_TOKEN}",
            'web_session': web_session,
        }
        payload = {
            'jsonrpc': '2.0',
            'method': 'user.profile',
            'id': 321
        }
        try:
            resp = requests.post(
                'https://api.click.uz/integration',
                json=payload, headers=headers, timeout=10
            )
            data = resp.json()
            if 'result' in data and 'error' not in data:
                user_data = data['result']
                user, created = User.objects.get_or_create(
                    phone=user_data.get('phone_number'),
                    defaults={
                        'first_name': user_data.get('name'),
                        'source': 'click_app',
                        'last_name': user_data.get('surname')
                    }
                )
                token = RefreshToken.for_user(user)
                return Response(
                    {
                        'access_token': str(token.access_token),
                        'refresh_token': str(token) 
                    }
                )
            return Response(data, status=400)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=500)