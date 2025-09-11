from payme.views import PaymeWebHookAPIView
from apps.payment.models.models import Orders, Payments
from payme.models import PaymeTransactions



class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def handle_created_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction created for this params: {params} and cr_result: {result}")

    def handle_successfully_payment(self, params, result, *args, **kwargs):
        
        try:
            trans_id = params.get('id')  
            
            transaction = PaymeTransactions.objects.filter(transaction_id=trans_id).first()
    

            payment = Payments.objects.filter(trans_id=transaction.account_id).first()
            if not payment:
                print(f"\nPayment with trans_id {trans_id} not found\n")
                return
            order = payment.order

            order.status = True
            order.save()

            payment.status = True
            payment.save()

            print(f"\nOrder {order.id} va Payment {payment.id} status True qilindi")
            print(f"Params: {params}")

        except Exception as e:
            print(f"===========\n\n{e}\n\n========================")
                

        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction successfully performed for this params: {params} and performed_result: {result}")

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        """
        Handle the cancelled payment. You can override this method
        """
        print(f"Transaction cancelled for this params: {params} and cancelled_result: {result}")