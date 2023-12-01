from typing import Optional, Union

import hvac.adapters
import hvac.exceptions

from cloud_storage_clients.connector import Connector
from cloud_storage_clients.exceptions import RepositoryError
from cloud_storage_clients.repositories import vault_adapter
from cloud_storage_clients.repositories.credentials import CredentialRepository
from cloud_storage_clients.repositories.vault_adapter import DefaultVaultAdapter


class VaultCredentialRepository(CredentialRepository):
    """
    This repository can be used to read credentials through a (Vault)[https://www.vaultproject.io/] secrets manager.
    It needs a VaultAdapter, that you can instantiate and give to constructor, or use method build() to directly
    instantiate this repository.
    A VaultAdapter class should implement at least get_secrets(vault_key: str).

    By default, this repository will build a vault key from given connector id and add a prefix to it.
    """

    def __init__(
        self, adapter: vault_adapter.VaultAdapter, prefix: Optional[str] = None
    ):
        self.prefix = prefix or ""
        self.adapter = adapter

    @staticmethod
    def build(
        url: str,
        *,
        vault_client: Optional[hvac.Client] = None,
        credentials: Union[
            vault_adapter.TokenCredentials, vault_adapter.SecretCredentials, None
        ] = None,
        hvac_client_verify: bool = True,
        secret_mount: Optional[str] = None,
        hvac_adapter: type[hvac.adapters.Adapter] = hvac.adapters.JSONAdapter,
        prefix: Optional[str] = None,
    ):
        adapter = DefaultVaultAdapter(
            url,
            vault_client=vault_client,
            credentials=credentials,
            hvac_client_verify=hvac_client_verify,
            secret_mount=secret_mount,
            hvac_adapter=hvac_adapter,
        )
        return VaultCredentialRepository(adapter, prefix)

    def get_credentials(self, connector: Connector) -> dict:
        vault_key = self.build_vault_key(connector)
        try:
            return self.adapter.get_secrets(vault_key)
        except Exception as e:
            raise RepositoryError(
                f"Could not retrieve credentials of connector {connector.key} from Vault"
            ) from e

    def update_credentials(self, connector: Connector, secret_data: dict) -> dict:
        vault_key = self.build_vault_key(connector)
        try:
            return self.adapter.update_secrets(vault_key, secret_data)
        except Exception as e:
            raise RepositoryError(
                f"Could not update credentials of connector {connector.key} from Vault"
            ) from e

    def delete_credentials(self, connector: Connector) -> dict:
        vault_key = self.build_vault_key(connector)
        try:
            return self.adapter.delete_secrets(vault_key)
        except Exception as e:
            raise RepositoryError(
                f"Could not delete credentials of connector {connector.key} from Vault"
            ) from e

    def build_vault_key(self, connector: Connector):
        vault_path = connector.key

        if self.prefix:
            vault_path = f"{self.prefix}/{vault_path}"

        return vault_path
