import logging

from spaceone.core.manager import BaseManager

_LOGGER = logging.getLogger(__name__)


class CryptoManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def collect_resources(self, options, secret_data, schema):
        pass
