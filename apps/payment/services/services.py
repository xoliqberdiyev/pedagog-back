import os
from decimal import Decimal
from typing import Union, Literal, TypeAlias, Tuple, Dict
from uuid import uuid4

import requests
from django.conf import settings
from django.utils.translation import gettext as _

from apps.pedagog.models.electron_resource import ElectronResource
from apps.shared.utils.logger import logger

Methods: TypeAlias = Literal[
    "receipt.account.create.transfer",
    "account.transfer.balance",
    "receipt.account.confirm.transfer",
]
GenerateAction: TypeAlias = Literal["uuid", "ext"]
AmountConvert: TypeAlias = Literal["decode", "encode"]
Currency: TypeAlias = Literal["uzs", "tiyin"]


def user_media_downloads(user):
    if not user.downloaded_media.exists():
        return 0
    return settings.MEDIA_AMOUNT / user.downloaded_media.count()


def send_money_to_moderator(moderator, amount) -> str | int | None:
    from apps.payment.models.models import TransactionModel

    card_number = moderator.card_number
    amount = Decimal(amount)

    if amount is None:
        raise Exception("Invalid amount: Amount cannot be None")

    paid_amount = moderator.paid_amount + amount
    service = UzumService()

    if card_number is None:
        raise Exception("Card number not found")

    transaction = TransactionModel.objects.create(
        status="pending", moderator=moderator, amount=amount
    )

    try:
        transaction_id = None
        transaction_id = service.create_transaction(float(amount), card_number).get(
            "id", None
        )
        if transaction_id is None:
            raise Exception("Transaction created error")
        service.confirm_transaction(transaction_id)

        transaction.status = "success"
        transaction.transaction_id = transaction_id
        moderator.paid_amount = paid_amount
        moderator.save()
        transaction.save()
        print(f"Pul {amount} so'm {card_number} kartasiga yuborildi")
        return transaction_id
    except Exception as e:
        transaction.status = "error"
        transaction.error = str(e)
        transaction.save()
        raise e

    return None


def get_user_profit(user):
    if not hasattr(user, "moderator"):
        return None
    paid_amount = user.moderator.paid_amount  # avval to'langan summa
    try:
        medias = (
            user.media.prefetch_related("download_users")
            .prefetch_related("user__downloaded_media")
            .all()
        )
        profit: int = 0
        for media in medias:
            for user in media.download_users.all():
                profit += user_media_downloads(user)
        return profit - paid_amount
    except Exception as e:
        logger.error(str(e))
    return 0


def get_profit_from_media(media):
    try:
        profit: int = 0
        for user in media.download_users.all():
            profit += user_media_downloads(user)
        return profit
    except Exception as e:
        logger.error(str(e))
    return 0


def get_user_statistics(user):
    try:
        medias = (
            user.media.prefetch_related("download_users")
            .prefetch_related("user__downloaded_media")
            .all()
        )
        downloads_count = 0
        resource_count = 0

        for media in medias:
            for download_user in media.download_users.all():
                if download_user == user:
                    downloads_count += 1

        resource_count = ElectronResource.objects.filter(user=user).count()

        return downloads_count, resource_count
    except Exception:
        return 0, 0


class UzumService:
    _number: Union[int, str]
    _mfo: Union[int, str]
    _sender_name: str
    _balance: int = None
    _errors: Dict = {
        "not_enough_balance": _("Not enough balance"),
        "status_error": _("Status error"),
        "transaction_not_found": _("Transaction not found"),
        "internal_error": _("Internal error"),
    }

    def __init__(self):
        self.uzum_id = os.getenv("UZUM_ID")
        self.uzum_key = os.getenv("UZUM_KEY")
        self._number = os.getenv("UZUM_NUMBER")
        self._mfo = os.getenv("UZUM_MFO")
        self._sender_name = os.getenv("UZUM_SENDER_NAME")
        self.lang = "uz-UZ"

    @property
    def balance(self) -> int:
        if self._balance:
            return self._balance
        return self._get_balance()

    def generate_link(
            self,
            client_id: str,
            order_id: str,
            amount: int,
            detail: str,
    ) -> Tuple:
        url = "https://checkout-key.inplat-tech.com/api/v1/payment/register"

        payload = {
            "successUrl": "https://my.pedagog.uz/history/",
            "failureUrl": "https://my.pedagog.uz/payment/",
            "viewType": "WEB_VIEW",
            "clientId": str(client_id),
            "currency": 860,
            "paymentDetails": detail,
            "orderNumber": str(order_id),
            "sessionTimeoutSecs": 600,
            "amount": amount * 100,
            "merchantParams": {
                "divisionId": "string",
                "divisionName": "string",
                "cart": {
                    "cartId": "1212",
                    "receiptType": "PURCHASE",
                    "items": [
                        {
                            "title": "string",
                            "productId": "string",
                            "quantity": 1,
                            "unitPrice": amount * 100,
                            "total": 1,
                            "receiptParams": {
                                "spic": "10305008002000000",
                                "packageCode": "1514296",
                                "vatPercent": 0,
                                "TIN": "207154122",
                            },
                        }
                    ],
                    "total": 1,
                },
            },
            "paymentParams": {
                "operationType": "PAYMENT",
                "payType": "ONE_STEP",
                "force3ds": True,
            },
        }

        headers = {
            "X-Terminal-Id": self.uzum_id,
            "X-API-Key": self.uzum_key,
            "Content-Language": self.lang,
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception("Status kod 200 emas")

        logger.info(response.json())
        data = response.json().get("result", {})
        trans_id = data.get("orderId")
        redirect_url = data.get("paymentRedirectUrl")

        if not trans_id or not redirect_url:
            raise Exception("Ma'lumotlar kutilgan formatda emas")

        return trans_id, redirect_url

    def create_transaction(self, amount: int, receiver_number: Union[int, str]) -> Dict:
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        ext_id: str = self._generate("ext")
        params: Dict = {
            "amount": self._amount_to_tiyin(amount),
            "ext_id": f"3:{ext_id}",
            "account": {"number": self._number, "mfo": self._mfo},
            "sender": {
                "id": f"topup-pedagog:{ext_id}",
                "name": self._sender_name,
            },
            "receiver": {"number": str(receiver_number)},
        }

        return self._request("receipt.account.create.transfer", params)

    def confirm_transaction(self, transaction_id: Union[str, int]) -> Dict:
        params = {"id": transaction_id}
        return self._request("receipt.account.confirm.transfer", params)

    def _request(self, method: Methods, params: Dict) -> Dict:
        url = "https://topup.apelsin.uz/api/v2/merchant"
        payload = {
            "jsonrpc": "2.0",
            "id": self._generate("uuid"),
            "method": method,
            "params": params,
        }
        headers = {
            "authorization": "Basic dG9wdXAtY2xhc3Njb206e0NrLlsxay9eSklp4oCT4oCTckFPRnZ+UEJMZSRndDgxXFp+",
            "content-type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers)
        logger.error("======= LOG ========")
        logger.error(payload)
        logger.error(params)
        logger.error(response.json())
        logger.error("===============")
        if response.status_code != 200:
            raise Exception(self._errors["status_error"])
        response_json = response.json()
        if result := response_json.get("result"):
            return result
        elif error := response_json.get("error"):
            raise Exception(error)
        raise Exception(self._errors["internal_error"])

    def _amount_to_tiyin(self, amount: int) -> int:
        return int(amount * 100)

    def _amount_to_uzs(self, amount: int) -> float:
        return amount / 100

    def _generate(self, action: GenerateAction) -> str:
        if action == "uuid":
            return str(uuid4())
        else:
            return str(uuid4())

    def _get_balance(self, currency: Currency = "uzs") -> int:
        params: Dict = {"number": self._number, "mfo": self._mfo}
        response = self._request("account.transfer.balance", params)
        balance = response["account"]["balance"]
        self._balance = balance
        if currency == "uzs":
            return self._amount_to_uzs(balance)
        return balance


class ChatService:
    def __init__(self, context=None):
        self.context = context or {}

    def call(self, data):
        connection_id = data.get("data", {}).get("connection_id")
        chat_id = data.get("chat")
        message = data.get("data", {}).get("message")

        if not connection_id or not chat_id or not message:
            return {"error": "Missing data fields (connection_id, chat_id, message)"}

        import importlib

        def get_user_serializer(user):
            module_path, class_name = (
                "core.http.serializers.user",
                "UserSerializer",
            )
            module = importlib.import_module(module_path)
            UserSerializer = getattr(module, class_name)
            return UserSerializer(user).data

        return {
            "connection_id": connection_id,
            "chat_id": chat_id,
            "message": message,
            "user": get_user_serializer(self.context.get("user")),
        }

    def action(self, data):
        action_type = data.get("action")
        if action_type == "call":
            return self.call(data)
        return {}

    def process(self, data) -> dict:
        response = self.action(data)
        chat = data.get("chat")
        if not chat:
            return {"error": "Missing chat"}

        return {
            "chat": f"chat_{chat}",
            "data": response,
        }
