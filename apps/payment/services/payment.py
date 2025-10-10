from click_up import ClickUp
from payme import Payme
from .services import UzumService
from apps.payment.utils.encode_url import encode_url
import os




class PaymentService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.click_up = ClickUp(
            service_id=os.getenv("CLICK_SERVICE_ID"),
            merchant_id=os.getenv("CLICK_MERCHANT_ID"),
        )
        # self.click_up_2 = ClickUp(
        #     service_id=os.getenv('CLICK_SERVICE_2_ID'),
        #     merchant_id=os.getenv('CLICK_MERCHANT_2_ID'),
        # )
        self.service_id = os.getenv('CLICK_SERVICE_ID')
        self.merchant_id = os.getenv("CLICK_MERCHANT_ID")
        self.service_id_2 = os.getenv('CLICK_SERVICE_2_ID')
        self.merchant_id_2 = os.getenv('CLICK_MERCHANT_2_ID')
        self.payme = Payme(payme_id=os.getenv("PAYME_ID"))

    def generate_link(self, order, payment_type, base_url):
        if payment_type == "click":
            pay_link = self.click_up.initializer.generate_pay_link(
                id=int(order.id),
                amount=order.price,
                return_url=f"{base_url}",
            )
            url = "https://my.click.uz/services/pay/"
            pay_link = (
                f"{url}?service_id={self.service_id}&merchant_id={self.merchant_id}" # noqa
                f"&amount={order.price}&transaction_param={order.id}"
                f"&return_url={base_url}"
            )
            trans_id = getattr(pay_link, "transaction_id", None) or str(order.id)  
            return trans_id, pay_link 
        
        elif payment_type == 'click_2':
            url = "https://my.click.uz/services/pay/"
            pay_link = (
                f"{url}?service_id={self.service_id_2}&merchant_id={self.merchant_id_2}" # noqa
                f"&amount={order.price}&transaction_param={order.id}"
                f"&return_url={encode_url(base_url)}"
            )
            # pay_link = self.click_up_2.initializer.generate_pay_link(
            #     id=int(order.id),
            #     amount=order.price,
            #     return_url=f"{base_url}"
            # )
            trans_id = getattr(pay_link, 'transaction_id', None) or str(order.id)
            return trans_id, pay_link

        elif payment_type == "payme":
            pay_link = self.payme.initializer.generate_pay_link(
                id=int(order.id),
                    amount=order.price,
                    return_url=f"{base_url}",
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
