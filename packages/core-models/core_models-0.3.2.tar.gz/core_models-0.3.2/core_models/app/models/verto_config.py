from django.db import models

from .company import Company
from .base import BaseModelAbstract


class VertoConfig(BaseModelAbstract, models.Model):
    company = models.OneToOneField(Company, models.CASCADE,
                                   related_name='verto_config')
    email = models.EmailField(null=False, blank=False)
    api_key = models.CharField(max_length=255, null=False, blank=False)
    client_id = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
        return self.email
