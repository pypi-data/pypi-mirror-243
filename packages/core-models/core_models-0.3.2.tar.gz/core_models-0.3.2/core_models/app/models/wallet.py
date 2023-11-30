import time

from django.db import models
from django.utils import timezone

from . import Company
from .base import BaseModelAbstract
from ... import constants


class Wallet(BaseModelAbstract, models.Model):
    created_by = None
    company = models.ForeignKey(Company, models.CASCADE,
                                related_name='wallets')
    currency = models.CharField(max_length=10)
    total_balance = models.DecimalField(default=0, decimal_places=2,
                                        max_digits=30)
    available_balance = models.DecimalField(default=0, decimal_places=2,
                                            max_digits=30)

    def __unicode__(self):
        return f"{self.company}'s {self.currency} Wallet"


class WalletTransaction(BaseModelAbstract, models.Model):
    wallet = models.ForeignKey(Wallet, models.CASCADE,
                               related_name='transactions')
    total_balance_before = models.DecimalField(decimal_places=2, max_digits=30)
    total_balance_after = models.DecimalField(decimal_places=2, max_digits=30)
    available_balance_before = models.DecimalField(decimal_places=2,
                                                max_digits=30)
    available_balance_after = models.DecimalField(decimal_places=2,
                                                  max_digits=30)
    amount = models.DecimalField(decimal_places=2, max_digits=30)
    type = models.CharField(choices=constants.TRANSACTION_TYPES)
    reference = models.CharField(max_length=255, editable=False)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return f"{self.wallet} | {self.reference}"

    def save(self, keep_deleted=False, **kwargs):
        if not self.reference:
            now = timezone.now()
            self.reference = now.strftime('%Y%m%d%H%M%S')
        self.total_balance_before = self.wallet.total_balance
        self.available_balance_before = self.wallet.available_balance

        if self.type == constants.DEBIT_TRANSACTION:
            self.wallet.total_balance -= self.amount
            self.wallet.available_balance -= self.amount
        else:
            self.wallet.total_balance += self.amount
            self.wallet.available_balance += self.amount

        self.total_balance_after = self.wallet.total_balance
        self.available_balance_after = self.wallet.available_balance
        self.wallet.save()
        super().save(keep_deleted=keep_deleted, **kwargs)
