from django.db import models
from django.utils import timezone

from .invoice import Invoice
from .company import Company
from .base import BaseModelAbstract
from ... import constants
from ...utils import random_numbers


class Payment(BaseModelAbstract, models.Model):
    payer = models.ForeignKey(Company, models.SET_NULL, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, models.SET_NULL, null=True,
                                blank=True, related_name='payments')
    expected_amount = models.DecimalField(decimal_places=2, max_digits=30)
    amount = models.DecimalField(decimal_places=2, max_digits=30, default=0)
    fees = models.DecimalField(decimal_places=2, max_digits=30, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=30, default=0)
    reference = models.CharField(max_length=100, )
    full_payment = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=constants.TXN_STATUSES,
                              default=constants.PENDING_TXN_STATUS)
    gateway = models.CharField(max_length=30, choices=constants.PAYMENT_GTW, null=True,
                               blank=True)
    gateway_response = models.TextField(blank=True, null=True)
    gateway_reference = models.CharField(max_length=255, null=True, blank=True)
    verdict = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.reference

    def save(self, keep_deleted=False, **kwargs):
        if not self.reference:
            now = timezone.now()
            x = random_numbers(2)
            self.reference = now.strftime('%Y%m%d%H%M%S') + str(x)
        super().save(keep_deleted=keep_deleted, **kwargs)
