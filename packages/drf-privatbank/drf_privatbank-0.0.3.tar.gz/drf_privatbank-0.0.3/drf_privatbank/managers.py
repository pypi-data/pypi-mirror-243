import requests
from datetime import datetime
import json

from .models import Privatbank
from .config import (
    PRIVATBANK_BALANCE_URI,
    PRIVATBANK_BALANCE_URI_BODY,
    PRIVATBANK_STATEMENT_URI,
    PRIVATBANK_STATEMENT_URI_BODY,
    PRIVATBANK_PAYMENT_URI,
    PRIVATBANK_CURRENCY_CASHE_RATE_URI,
    PRIVATBANK_CURRENCY_NON_CASHE_RATE_URI,
    
    DOCUMENT_NUMBER,
    DOCUMENT_TYPE,
    PAYMENT_CCY,
    PAYMENT_DESTINATION,
    PAYMENT_NAMING,
    RECIPIENT_IFI,
    RECIPIENT_IFI_TEXT,
    RECIPIENT_NCEO,
    DAY_UTC,
)


class PrivatManager:

    def __init__(self, request):
        self.request = request

    @staticmethod
    def get_privat_object(request):
        user = request.user
        privat_obj = Privatbank.objects.filter(user=user)
        return privat_obj
    
    @classmethod
    def get_currency(cls, cashe_rate: bool):
        if cashe_rate:
            uri = PRIVATBANK_CURRENCY_CASHE_RATE_URI
        else:
            uri = PRIVATBANK_CURRENCY_NON_CASHE_RATE_URI
        _ = requests.get(uri)
        return _.status_code, _.json()

    @classmethod
    def get_client_info(cls, token: str, iban: str):
        date = cls.__date(0)
        uri = PRIVATBANK_BALANCE_URI_BODY.format(
            PRIVATBANK_BALANCE_URI,
            iban,
            date
        )
        headers = {"token": token}
        _ = requests.get(uri, headers=headers)
        _status = _.status_code
        payload = _.json()
        return _status, payload

    @classmethod
    def get_balance(cls, token: str, iban: str):
        _status, payload = cls.get_client_info(token, iban)
        if _status == 200:
            balance = {
                "balance": payload["balances"][0]["balanceOutEq"]
            } 
            return _status, balance
        return _status, payload

    @classmethod
    def get_statement(cls, token: str, iban: str, period: int, limit: int):
        date = cls.__date(period)
        uri = PRIVATBANK_STATEMENT_URI_BODY.format(
            PRIVATBANK_STATEMENT_URI, iban, date, limit
        )
        headers = {"token": token}
        _ = requests.get(uri, headers=headers)
        return _.status_code, _.json()
        
    @classmethod
    def create_payment(cls, token: str, iban: str, recipient: str, amount: float):
        body = cls.__payment_body(recipient, amount, iban)
        data = json.dumps(body)
        headers = {"token": token}
        _ = requests.post(PRIVATBANK_PAYMENT_URI, headers=headers, data=data)
        return _.status_code, _.json()

    @staticmethod
    def __date(period: int):
        time_delta = int(datetime.now().timestamp()) - (period * DAY_UTC)
        dt_object = datetime.fromtimestamp(time_delta)
        year = dt_object.strftime("%Y")
        month = dt_object.strftime("%m")
        day = dt_object.strftime("%d")
        date = f"{day}-{str(month)}-{year}"
        return date
    
    @staticmethod
    def __payment_body(recipient: str, amount: float, iban: str):
        body = {
            "document_number": DOCUMENT_NUMBER,
            "recipient_card": recipient,
            "recipient_nceo": RECIPIENT_NCEO,
            "payment_naming": PAYMENT_NAMING,
            "payment_amount": amount,
            "recipient_ifi": RECIPIENT_IFI,
            "recipient_ifi_text": RECIPIENT_IFI_TEXT,
            "payment_destination": PAYMENT_DESTINATION,
            "payer_account": iban,
            "payment_ccy": PAYMENT_CCY,
            "document_type": DOCUMENT_TYPE
        }
        return body
