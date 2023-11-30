import requests

from core_models.utils import log_exception
from . import BaseVertoIntegration
from ..base_integration import BaseIntegrationParam


class VertoCreatePaymentIntegrationParam(BaseIntegrationParam):

    def __init__(self, beneficiary_id, purpose_id, amount,
                 wallet_id, reference, payment_id):
        self.beneficiary_id = beneficiary_id
        self.purpose_id = purpose_id
        self.amount = amount
        self.wallet_id = wallet_id
        self.reference = reference
        self.payment_id = payment_id


class VertoCreatePaymentIntegration(BaseVertoIntegration):
    def __init__(self, param: VertoCreatePaymentIntegrationParam):
        super().__init__(param)

    def execute(self) -> int:
        url = f"{self.base_url}/profile/v2.2/request"
        payload = {
          "beneficiaryId": self.beneficiary_id,
          "purposeId": self.purpose_id,
          "amount": self.amount,
          "walletId": self.wallet_id,
          "clientReference": self.reference,
          "paymentId": self.payment_id
        }
        headers = {
            "Authorization": f"Bearer {self.param.token}"
        }
        try:
            resp = requests.post(url, json=payload, headers=headers)
            if resp.ok:
                data = resp.json()
                if data['success']:
                    return data['payment']['id']
        except Exception as ex:
            log_exception('VertoAddBeneficiaryIntegration', ex)
        return 0
