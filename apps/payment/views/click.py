from click_up.views import ClickWebhook
from apps.payment.models.models import Orders, Payments


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

            print(f"\n\nOrder {order.id} va Payment {payment.id} status True qilindi\n\n{account_id}\n\n")
            print(f"Params: {params}")

        except Exception as e:
            print(f"===========\n\n{e}\n\n========================")

    def cancelled_payment(self, params):
        """
        cancelled payment method process you can ovveride it
        """
        print(f"payment cancelled params: {params}")