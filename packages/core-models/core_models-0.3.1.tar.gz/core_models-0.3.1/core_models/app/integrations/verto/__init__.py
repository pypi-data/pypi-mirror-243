from abc import ABCMeta

from ..base_integration import BaseIntegration


class BaseVertoIntegration(BaseIntegration):
    base_url = 'https://api-v3-sandbox.vertofx.com'

    class Meta(ABCMeta):
        pass
