import requests
from datetime import datetime
from .models import Mono
from .config import (
    MONO_CURRENCY_URI,
    MONO_CLIENT_INFO_URI,
    MONO_STATEMENT_URI,
    MONO_WEBHOOK_URI,
    DAY_UTC,
)


class MonoManager:

    def __init__(self, request):
        self.request = request

    @staticmethod
    def get_mono_object(request):
        user = request.user
        mono_obj = Mono.objects.filter(user=user)
        return mono_obj
    
    @classmethod
    def get_currency(cls):
        _ = requests.get(MONO_CURRENCY_URI)
        return _.status_code, _.json()

    @staticmethod
    def get_client_info_mono(token):
        headers = {"X-Token": token}
        _ = requests.get(MONO_CLIENT_INFO_URI, headers=headers)
        return _.status_code, _.json()

    @classmethod
    def get_balance_mono(cls, token):
        _status, payload = cls.get_client_info_mono(token)

        if _status == 200:
            balance = {
                'balance': payload["accounts"][0]["balance"] / 100
            }
            return _status, balance
        
        return _status, payload
        
    @staticmethod
    def get_statement_mono(token, period):
        time_delta = int(datetime.now().timestamp()) - (period * DAY_UTC)
        
        headers = {"X-Token": token}
        _ = requests.get(
            f"{MONO_STATEMENT_URI}{time_delta}/",
            headers=headers
        )
        _status = _.status_code
        payload = _.json()
        
        return _status, payload

    @staticmethod
    def create_webhook(token, webHookUrl):
        headers = {"X-Token": token}
        _ = requests.post(
            MONO_WEBHOOK_URI, data=webHookUrl, headers=headers
        )
        print(_.content)
        _status = _.status_code
        payload = _.json()
        return _status, payload
