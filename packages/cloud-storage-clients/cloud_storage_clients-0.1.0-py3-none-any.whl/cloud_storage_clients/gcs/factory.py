from typing import Optional

from cloud_storage_clients.connector import Connector
from cloud_storage_clients.gcs.client import GcsClient


class GcsClientFactory:
    def __call__(self, connector: Connector, credentials: Optional[dict]):
        return GcsClient(connector, credentials)
