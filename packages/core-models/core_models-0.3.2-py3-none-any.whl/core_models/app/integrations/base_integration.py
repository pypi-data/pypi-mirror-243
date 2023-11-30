from abc import ABC
from typing import Optional


class BaseIntegrationParam(ABC):
    pass


class BaseIntegration(ABC):
    base_url = ''

    def __init__(self, param: Optional[BaseIntegrationParam] = None):
        self.param = param

    def execute(self):
        pass
