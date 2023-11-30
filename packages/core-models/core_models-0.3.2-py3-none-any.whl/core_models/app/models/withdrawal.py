from django.db import models

from .wallet import Wallet
from .bank_account import BankAccount
from .base import BaseModelAbstract
from ... import constants


class Withdrawal(BaseModelAbstract, models.Model):
    wallet = models.ForeignKey(Wallet, models.CASCADE,
                               related_name='withdrawals')
    account = models.ForeignKey(BankAccount, models.CASCADE,
                                related_name='withdrawals')
    source_amount = models.DecimalField(max_digits=30, decimal_places=2)
    destination_amount = models.DecimalField(max_digits=30, decimal_places=2)
    has_fx = models.BooleanField(default=False)
    reason = models.CharField(max_length=150)
    status = models.CharField(max_length=5, choices=constants.TXN_STATUSES,
                              default=constants.PENDING_TXN_STATUS)
    reference = models.CharField(max_length=100)
    gateway_reference = models.CharField(max_length=100, null=True, blank=True)
    gateway = models.CharField(max_length=30, choices=constants.PAYMENT_GTW,
                               null=True,
                               blank=True)
    gateway_response = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.reference
