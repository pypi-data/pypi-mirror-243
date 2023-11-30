import os
import time

from django.db import models
from django.utils import timezone
from model_utils import FieldTracker

from .notification import Notification
from .base import BaseModelAbstract
from .user import User
from ... import constants
from ...utils import send_contract_feedback_mail_to_seller


def contract_upload_to(instance, filename):
    f, ext = os.path.splitext(filename)
    return f'contracts/{instance.reference}/document{ext}'


class Contract(BaseModelAbstract, models.Model):
    seller = models.ForeignKey(User, models.SET_NULL, null=True, blank=True,
                               related_name='seller_contracts')
    buyer = models.ForeignKey(User, models.SET_NULL, null=True, blank=True,
                              related_name='buyer_contracts')
    reference = models.CharField(max_length=255, unique=True, null=False,
                                 blank=False)
    document = models.FileField(null=False, blank=False,
                                upload_to=contract_upload_to)
    status = models.CharField(max_length=1,
                              choices=constants.CONTRACT_STATUSES,
                              default=constants.PENDING_CONTRACT_STATUS)
    buyer_accepted_on = models.DateTimeField(null=True, blank=True)
    buyer_accepted_via = models.CharField(
        max_length=1, choices=constants.CONTRACT_ACCEPTANCE_CHANNELS,
        null=True, blank=True
    )
    tracker = FieldTracker(fields=['status'])

    class Meta:
        unique_together = (('seller', 'buyer'), )

    def __unicode__(self):
        return self.reference

    def save(self, keep_deleted=False, **kwargs):
        request = None
        user = None
        if 'request' in kwargs:
            request = kwargs.pop('request')
        if request:
            user = request.user
        if not self.reference:
            self.reference = f"LQCT{time.time_ns()}"
        if self.status == constants.ACCEPTED_CONTRACT_STATUS:
            self.buyer_accepted_on = timezone.now()
        status_changed = self.tracker.has_changed('status')
        super(Contract, self).save(keep_deleted, **kwargs)
        if status_changed:
            log = ContractStatusLog(
                contract=self,
                status=self.status,
                created_by=user
            )
            log.save(request=request)

    def accept(self, channel: str):
        self.buyer_accepted_on = timezone.now()
        self.buyer_accepted_via = channel
        self.accepted = True
        self.save()


def doc_upload_to(instance, filename):
    f, ext = os.path.splitext(filename)
    return f'contracts/{instance.contract.reference}/{instance.pk}{ext}'


class ContractDocument(BaseModelAbstract, models.Model):
    contract = models.ForeignKey(Contract, models.CASCADE)
    file = models.FileField(null=False, blank=False, upload_to=doc_upload_to)
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = "Contract Document"
        verbose_name_plural = "Contract Documents"

    def __unicode__(self):
        return f"{self.contract.reference} - {self.name}"


class ContractStatusLog(BaseModelAbstract, models.Model):
    contract = models.ForeignKey(Contract, models.CASCADE)
    status = models.CharField(max_length=1,
                              choices=constants.CONTRACT_STATUSES)
    reason = models.TextField(null=True, blank=True)
    tracker = FieldTracker(fields=['status'])

    def __unicode__(self):
        return f"Status: {self.status} of Contract: {self.contract}"

    def save(self, keep_deleted=False, **kwargs):
        request = None
        user = None
        if 'request' in kwargs:
            request = kwargs.pop('request')
        if request:
            user = request.user
        status_changed = self.tracker.has_changed('status')
        super(ContractStatusLog, self).save(keep_deleted, **kwargs)
        if self.status == constants.VERIFIED_CONTRACT_STATUS:
            Notification.objects.create(
                object_id=self.id,
                notice_type=constants.CONTRACT_CONFIRMED_NOTIF_TYPE,
                created_by=user
            )
        if request and self.status not in [
            constants.PENDING_CONTRACT_STATUS,
            constants.ACCEPTED_CONTRACT_STATUS
        ]:
            send_contract_feedback_mail_to_seller(
                self.contract, self, request
            )


class ContractInformation(BaseModelAbstract, models.Model):
    contract = models.OneToOneField(Contract, models.CASCADE,
                                    related_name="information")
    length_of_relationship = models.CharField(max_length=100, null=True,
                                              blank=True)
    type_of_product = models.CharField(max_length=100, null=True, blank=True)
    total_volume_of_invoices = models.IntegerField(default=0)
    total_value_of_invoices = models.DecimalField(
        decimal_places=2, max_digits=30, default=0
    )
    invoices_amount_paid = models.DecimalField(
        decimal_places=2, max_digits=30, default=0
    )
    total_deductions = models.DecimalField(
        decimal_places=2, max_digits=30, default=0
    )
    supply_chain = models.ForeignKey(
        ContractDocument, models.SET_NULL, null=True, blank=True,
        related_name='supply_chain'
    )
    bank_statement = models.ForeignKey(
        ContractDocument, models.SET_NULL, null=True, blank=True,
        related_name='bank_statement'
    )
    credit_notes = models.ForeignKey(
        ContractDocument, models.SET_NULL, null=True, blank=True,
        related_name='credit_notes'
    )
    completed = models.BooleanField(default=False, editable=False)

    def __unicode__(self):
        return f"{self.contract}'s Information"

    def save(self, keep_deleted=False, **kwargs):
        self.completed = all(
            [self.length_of_relationship,
             self.type_of_product,
             self.supply_chain,
             self.bank_statement,
             self.credit_notes]
        )
        super().save(keep_deleted, **kwargs)
