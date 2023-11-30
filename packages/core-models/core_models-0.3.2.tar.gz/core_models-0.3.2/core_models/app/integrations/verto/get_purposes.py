from typing import List

import requests

from core_models.utils import log_exception
from . import BaseVertoIntegration
from ..base_integration import BaseIntegrationParam

purposes = []


class VertoPurpose:
    def __init__(self, purpose_id: int, purpose: str):
        self.purpose_id = purpose_id
        self.purpose = purpose

    def to_dict(self):
        return {
            "purpose_id": self.purpose_id,
            "purpose": self.purpose,
        }


class VertoGetPurposesIntegrationParam(BaseIntegrationParam):

    def __init__(self, token):
        self.token = token


class VertoGetPurposesIntegration(BaseVertoIntegration):

    def __init__(self, param: VertoGetPurposesIntegrationParam):
        super().__init__(param)

    def execute(self) -> List[VertoPurpose]:
        global purposes
        if bool(purposes):
            return purposes

        url = f"{self.base_url}/profile/v2.1/purpose?purpose=true"
        headers = {
            "Authorization": f"Bearer {self.param.token}"
        }
        _purposes = []
        try:
            resp = requests.get(url, headers=headers)
            if resp.ok:
                data = resp.json()
                if data['success']:
                    for item in data['documentTypes']:
                        _purposes.append(VertoPurpose(
                            purpose_id=item['id'],
                            purpose=item['title'],
                        ))
                    purposes = _purposes
        except Exception as ex:
            log_exception('VertoGetPurposesIntegration', ex)
        return _purposes
