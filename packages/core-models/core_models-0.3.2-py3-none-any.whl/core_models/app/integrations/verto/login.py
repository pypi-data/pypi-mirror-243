import requests

from core_models.utils import log_exception
from . import BaseVertoIntegration
from ..base_integration import BaseIntegrationParam


class VertoLoginIntegrationParam(BaseIntegrationParam):

    def __init__(self, api_key, client_id):
        self.api_key = api_key
        self.client_id = client_id


class VertoLoginIntegration(BaseVertoIntegration):

    def __init__(self, param: VertoLoginIntegrationParam):
        super().__init__(param)

    def execute(self):
        url = f"{self.base_url}/users/login"
        payload = {
            "apiKey": self.param.api_key,
            "clientId": self.param.client_id,
            "mode": "apiKey"
        }
        print(['VertoLoginIntegration', payload])
        try:
            resp = requests.post(url, json=payload)
            if resp.ok:
                data = resp.json()
                if data['success']:
                    return data['token']
        except Exception as ex:
            log_exception('VertoLoginIntegration', ex)
        return None
