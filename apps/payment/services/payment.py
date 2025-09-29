from click_up import ClickUp
from payme import Payme
from .services import UzumService

import os




class PaymentService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.click_up = ClickUp(
            service_id=os.getenv("CLICK_SERVICE_ID"),
            merchant_id=os.getenv("CLICK_MERCHANT_ID"),
        )
        self.click_up_2 = ClickUp(
            service_id=os.getenv('CLICK_SERVICE_2_ID'),
            merchant_id=os.getenv('CLICK_MERCHANT_2_ID'),
        )
        self.payme = Payme(payme_id=os.getenv("PAYME_ID"))

    def generate_link(self, order, payment_type):
        print(payment_type)

        if payment_type == "click":
            pay_link = self.click_up.initializer.generate_pay_link(
                id=int(order.id),
                amount=order.price,
                return_url="https://pedagog.uz",
            )
            trans_id = getattr(pay_link, "transaction_id", None) or str(order.id)  
            return trans_id, pay_link 
        
        elif payment_type == 'click_2':
            pay_link = self.click_up_2.initializer.generate_pay_link(
                id=int(order.id),
                amount=order.price,
                return_url='https://pedagog.uz'
            )
            trans_id = getattr(pay_link, 'transaction_id', None) or str(order.id)
            return trans_id, pay_link

        elif payment_type == "payme":
            pay_link = self.payme.initializer.generate_pay_link(
                id=int(order.id),
                    amount=order.price,
                    return_url="https://pedagog.uz",
            )
            trans_id = getattr(pay_link, "transaction_id", None) or str(order.id)
            return trans_id, pay_link

        else:
            trans_id, redirect_url = UzumService().generate_link(
                self.user_id,
                order.id,
                order.price,
                f"To'lov miqdori {order.price}, to'lov sanasi {order.created_at.strftime('%d-%m-%Y')}, "
                f"to'lov buyurtma raqami {order.id}, buyurtma {order.science}",
            )
            return trans_id, redirect_url
