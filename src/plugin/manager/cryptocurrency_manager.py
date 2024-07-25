import logging
import os

from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import (
    make_cloud_service,
    make_cloud_service_type,
    make_error_response,
    make_response,
)

from plugin.connector.cryptocurrency_connector import CryptoConnector

_LOGGER = logging.getLogger(__name__)
_CURRENT_DIR = os.path.dirname(__file__)
_METADATA_DIR = os.path.join(_CURRENT_DIR, "../metadata/")


class CryptoManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.provider = "portfolio"
        self.cloud_service_group = "Portfolio"
        self.cloud_service_type = "Cryptocurrency"
        self.metadata_path = os.path.join(
            _METADATA_DIR, "portfolio/cryptocurrency.yaml"
        )

    def collect_resources(self, options, secret_data, schema):
        try:
            yield from self.collect_cloud_service_type(options, secret_data, schema)
            yield from self.collect_cloud_service(options, secret_data, schema)
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

    def collect_cloud_service_type(self, options, secret_data, schema):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
        )

        yield make_response(
            cloud_service_type=cloud_service_type,
            match_keys=[["name", "reference.resource_id", "account", "provider"]],
            resource_type="inventory.CloudServiceType",
        )

    def collect_cloud_service(self, options, secret_data, schema):
        crypto_connector = CryptoConnector()
        cryptocurrencies = crypto_connector.list_cryptocurrencies()

        for crypto in cryptocurrencies:
            cloud_service = make_cloud_service(
                name=crypto["name"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=crypto,
                data_format="dict",
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
            )
