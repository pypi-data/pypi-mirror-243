from typing import Optional

from cloud_storage_clients.azure.client import AzureClient
from cloud_storage_clients.connector import Connector


class AzureClientFactory:
    def __init__(self, delegation_key_expiration_time: int):
        self.delegation_key_expiration_time = delegation_key_expiration_time

    def __call__(self, connector: Connector, credentials: Optional[dict]):
        return AzureClient(connector, credentials, self.delegation_key_expiration_time)
