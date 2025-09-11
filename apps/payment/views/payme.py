from payme.views import PaymeWebHookAPIView
from apps.payment.models.models import Orders, Payments


class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def handle_created_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction created for this params: {params} and cr_result: {result}")

    def handle_successfully_payment(self, params, result, *args, **kwargs):
        
        order_id = params.get('account', {}).get('order_id')
        trans_id = params.get('id')

        print(f"\n--- Payme Callback Received ---\norder_id: {order_id}\ntrans_id: {trans_id}\nparams: {params}\n-----------------------------\n")

        if order_id:
            try:
                order = Orders.objects.get(id=int(order_id))
                order.status = True
                order.save()
                print(f"\nOrder {order_id} status True qilindi\n")

                payment = Payments.objects.filter(order=order, trans_id=trans_id).first()
                if payment:
                    payment.status = True
                    payment.save()
                    print(f"\nPayment {payment.id} status True qilindi\n")
                else:
                    print(f"\nPayment mavjud emas, faqat Order yangilandi\n")

            except Orders.DoesNotExist:
                print(f"\nOrder with id {order_id} not found\n")
                
                

        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction successfully performed for this params: {params} and performed_result: {result}")

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        """
        Handle the cancelled payment. You can override this method
        """
        print(f"Transaction cancelled for this params: {params} and cancelled_result: {result}")