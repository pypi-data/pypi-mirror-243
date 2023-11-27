import requests

from core_models.utils import log_exception
from . import BaseVertoIntegration
from ..base_integration import BaseIntegrationParam


class VertoAddBeneficiaryIntegrationParam(BaseIntegrationParam):

    def __init__(self, beneficiary_type, currency, country_code,
                 account_number, bank_code, country_name, reference, token,
                 first_name="", last_name="",
                 company_name=""):
        self.beneficiary_type = beneficiary_type
        self.currency = currency
        self.country_code = country_code
        self.account_number = account_number
        self.bank_code = bank_code
        self.country_name = country_name
        self.reference = reference
        self.first_name = first_name
        self.last_name = last_name
        self.company_name = company_name
        self.token = token


class VertoAddBeneficiaryIntegration(BaseVertoIntegration):
    def __init__(self, param: VertoAddBeneficiaryIntegrationParam):
        super().__init__(param)

    def execute(self) -> int:
        url = f"{self.base_url}/profile/v2.1/beneficiaries"
        payload = {
            "beneficiaryEntityType": self.param.beneficiary_type,
            "beneficiaryFirstName": self.param.first_name,
            "beneficiaryLastName": self.param.last_name,
            "beneficiaryCompanyName": self.param.company_name,
            "currency": self.param.currency.upper(),
            "beneficiaryCountryCode": self.param.country_code.upper(),
            "accountNumber": self.param.account_number,
            "nationalId": self.param.bank_code,
            "country": self.param.country_name,
            "clientReference": self.param.reference
        }
        headers = {
            "Authorization": f"Bearer {self.param.token}"
        }
        try:
            resp = requests.post(url, json=payload, headers=headers)
            if resp.ok:
                data = resp.json()
                if data['success']:
                    return data['account']['id']
        except Exception as ex:
            log_exception('VertoAddBeneficiaryIntegration', ex)
        return 0
