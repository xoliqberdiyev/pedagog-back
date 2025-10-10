from datetime import timezone
import hashlib
from django.http import JsonResponse
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
        

class ClickCallbackView(views.APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        action = data.get("action")
        click_trans_id = data.get("click_trans_id")
        amount = data.get("amount")
        sign_string = data.get("sign_string")
        merchant_prepare_id = data.get("merchant_prepare_id")
        order_id = data.get("merchant_trans_id")
        service_id = data.get('service_id')
        sign_time = data.get('sign_time')
        print(f"action: {action}, click_trans_id: {click_trans_id}, amount: {amount}, sign_string: {sign_string}, merchant_prepare_id: {merchant_prepare_id}, order_id: {order_id}, service_id: {service_id}, sign_time: {sign_time}")

        current_config = None
        for name, conf in settings.CLICK_CONFIGS.items():
            if conf["SERVICE_ID"] == service_id:
                current_config = conf
                break

        if not current_config:
            print({"error": -8, "error_note": "Unknown merchant"})
            return JsonResponse({"error": -8, "error_note": "Unknown merchant"})

        check_sign = hashlib.md5(
            f"{click_trans_id}"
            f"{current_config['SERVICE_ID']}"
            f"{current_config['SECRET_KEY']}"
            f"{order_id}"
            f"{amount}"
            f"{action}"
            f"{sign_time}".encode('utf-8')
        ).hexdigest()
        print(f"check_sign: {check_sign}")

        if check_sign != sign_string:
            print({"error": -1, "error_note": "Sign mismatch"})
            return JsonResponse({"error": -1, "error_note": "Sign mismatch"})

        try:
            order = Orders.objects.get(id=order_id)
        except Orders.DoesNotExist:
            print({"error": -5, "error_note": "Order not found"})
            return JsonResponse({"error": -5, "error_note": "Order not found"})

        if action == "0":
            order.status = False
            order.save()
            return JsonResponse({
                "error": 0,
                "error_note": "Success",
                "click_trans_id": click_trans_id,
                "merchant_prepare_id": order.id,
            })

        elif action == "1":
            order.status = True
            order.paid_at = timezone.now()
            order.save()
            return JsonResponse({
                "error": 0,
                "error_note": "Payment confirmed",
                "click_trans_id": click_trans_id,
                "merchant_confirm_id": order.id,
            })
        print({"error": -2, "error_note": "Invalid action"})
        return JsonResponse({"error": -2, "error_note": "Invalid action"})