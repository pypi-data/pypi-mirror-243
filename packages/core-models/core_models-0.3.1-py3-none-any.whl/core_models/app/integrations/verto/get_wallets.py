from typing import List

import requests

from core_models.utils import log_exception
from . import BaseVertoIntegration
from ..base_integration import BaseIntegrationParam


class VertoWallet:
    def __init__(self, wallet_id: int, account_name: str, bic: str, iban: str,
                 account_number: str, bank: str, currency: str):
        self.wallet_id = wallet_id
        self.account_name = account_name
        self.bic = bic
        self.iban = iban
        self.account_number = account_number
        self.bank = bank
        self.currency = currency

    def to_dict(self):
        return {
            "wallet_id": self.wallet_id,
            "account_name": self.account_name,
            "bic": self.bic,
            "iban": self.iban,
            "account_number": self.account_number,
            "bank": self.bank,
            "currency": self.currency,
        }


class VertoGetWalletsIntegrationParam(BaseIntegrationParam):

    def __init__(self, token):
        self.token = token


class VertoGetWalletsIntegration(BaseVertoIntegration):
    def __init__(self, param: VertoGetWalletsIntegrationParam):
        super().__init__(param)

    def execute(self) -> List[VertoWallet]:
        url = f"{self.base_url}/profile/wallet"
        params = {
            "customPageSize": 10,
            "page": 1,
            "listAll": "false",
            "walletAccountMode": "INTERNATIONAL"
        }
        headers = {
            "Authorization": f"Bearer {self.param.token}"
        }
        wallets = []
        try:
            resp = requests.get(url, params=params, headers=headers)
            if resp.ok:
                data = resp.json()
                if data['success']:
                    for item in data['items']:
                        currency = item['currency']['currencyName']
                        _wallets = list(
                            filter(
                                lambda w: w['virtualAccount']['accountMode'] == 'INTERNATIONAL', item['walletAccounts']
                            )
                        )
                        for wallet in _wallets:
                            wallets.append(VertoWallet(
                                wallet_id=wallet['walletId'],
                                iban=wallet['virtualAccount']['iban'],
                                account_number=wallet['virtualAccount'][
                                    'accountNumber'],
                                bic=wallet['virtualAccount']['sortCode'],
                                account_name=wallet['virtualAccount']['name'],
                                currency=currency,
                                bank=wallet['virtualAccount']['provider']
                            ))
        except Exception as ex:
            log_exception('VertoGetWalletsIntegration', ex)
        return wallets
