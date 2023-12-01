from typing import Optional

from cloud_storage_clients.connector import Connector
from cloud_storage_clients.s3.client import S3Client


class S3ClientFactory:
    def __init__(self, default_region_name: Optional[str] = None):
        self.default_region_name = default_region_name

    def __call__(self, connector: Connector, credentials: Optional[dict]):
        return S3Client(connector, credentials, self.default_region_name)
