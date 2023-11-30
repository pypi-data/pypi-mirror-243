from typing import List

import requests

from core_models.utils import log_exception
from . import BaseVertoIntegration
from ..base_integration import BaseIntegrationParam

currencies = []


class VertoCurrency:
    def __init__(self, currency_id: int, name: str, code: str):
        self.currency_id = currency_id
        self.code = code
        self.name = name

    def to_dict(self):
        return {
            "id": str(self.currency_id),
            "name": self.name,
            "code": self.code,
        }


class VertoGetCurrenciesIntegrationParam(BaseIntegrationParam):

    def __init__(self, token):
        self.token = token


class VertoGetCurrenciesIntegration(BaseVertoIntegration):

    def __init__(self, param: VertoGetCurrenciesIntegrationParam):
        super().__init__(param)

    def execute(self) -> List[VertoCurrency]:
        global currencies
        if bool(currencies):
            return currencies

        url = f"{self.base_url}/profile/v2.1/currencies?customPageSize=999" \
              f"&page=1"
        headers = {
            "Authorization": f"Bearer {self.param.token}"
        }
        _currencies = []
        try:
            resp = requests.get(url, headers=headers)
            if resp.ok:
                data = resp.json()
                if data['success']:
                    for item in data['data']:
                        _currencies.append(VertoCurrency(
                            currency_id=item['id'],
                            name=item['countryName'],
                            code=item['currencyName'],
                        ))
                    currencies = _currencies
        except Exception as ex:
            log_exception('VertoGetCurrenciesIntegration', ex)
        return _currencies
