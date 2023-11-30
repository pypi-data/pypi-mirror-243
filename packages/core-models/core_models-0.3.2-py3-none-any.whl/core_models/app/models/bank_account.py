from django.db import models

from .company import Company
from .country import Country
from .base import BaseModelAbstract
from ... import constants


class BankAccount(BaseModelAbstract, models.Model):
    company = models.ForeignKey(
        Company, models.SET_NULL, null=True, blank=True
    )
    account_type = models.CharField(choices=constants.BANK_ACCOUNT_TYPES,
                                    default=constants.CORPORATE_BANK_ACCOUNT)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    sort_code = models.CharField(max_length=20)
    country = models.ForeignKey(Country, models.SET_NULL, null=True,
                                blank=True)
    third_party_id = models.CharField(null=True, blank=True, editable=False)

    def __unicode__(self):
        return f"{self.company}|{self.bank_name}|{self.account_number}|{self.sort_code}"
