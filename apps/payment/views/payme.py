from payme.views import PaymeWebHookAPIView
from apps.payment.models.models import Orders, Payments


class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def handle_created_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction created for this params: {params} and cr_result: {result}")

    def handle_successfully_payment(self, params, result, *args, **kwargs):
        
        print(f"Transaction successfully performed for params: {params} and performed_result: {result}")
        
        order_id = params.get('order_id')
        trans_id = params.get('id')  

        if order_id:
            try:
                order = Orders.objects.get(id=order_id)
                order.status = True
                order.save()

                payment = Payments.objects.filter(order=order, trans_id=trans_id).first()
                if payment:
                    payment.status = True
                    payment.save()
                    print(f"Payment {payment.id} muvaffaqiyatli yangilandi")
                else:
                    print(f"Payment mavjud emas, faqat Order yangilandi")

                print(f"Order {order_id} muvaffaqiyatli yangilandi")
            except Orders.DoesNotExist:
                print(f"Order with id {order_id} not found")
                
                

        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction successfully performed for this params: {params} and performed_result: {result}")

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        """
        Handle the cancelled payment. You can override this method
        """
        print(f"Transaction cancelled for this params: {params} and cancelled_result: {result}")