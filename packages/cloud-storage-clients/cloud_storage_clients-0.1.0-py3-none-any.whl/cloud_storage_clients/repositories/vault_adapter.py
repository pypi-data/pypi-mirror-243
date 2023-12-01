import abc
import logging
from dataclasses import dataclass
from typing import Optional, Union

import hvac
import hvac.adapters
import hvac.exceptions


class VaultAdapter(abc.ABC):
    """This class can be implemented to connect to a Vault secrets manager.
    It will be used by a VaultCredentialRepository to access and retrieve secrets holding connectors credentials.
    """

    @abc.abstractmethod
    def get_secrets(self, vault_key: str):
        pass

    @abc.abstractmethod
    def update_secrets(self, vault_key: str, secret_data: dict):
        pass

    @abc.abstractmethod
    def delete_secrets(self, vault_key: str):
        pass


@dataclass
class SecretCredentials:
    role_id: str
    secret_id: str


@dataclass
class TokenCredentials:
    token: str
    unseal_key: str


class DefaultVaultAdapter(VaultAdapter):
    def __init__(
        self,
        url: str,
        *,
        vault_client: Optional[hvac.Client] = None,
        credentials: Union[SecretCredentials, TokenCredentials, None] = None,
        hvac_client_verify: bool = True,
        secret_mount: Optional[str] = None,
        hvac_adapter: type[hvac.adapters.Adapter] = hvac.adapters.JSONAdapter,
    ):
        self.url = url
        self.hvac_client_verify = hvac_client_verify
        self.secret_mount = secret_mount or ""

        if vault_client:
            self.client = vault_client
        elif isinstance(credentials, SecretCredentials):
            self.client = self.get_hvac_client_from_secret(
                url, credentials, hvac_adapter, hvac_client_verify
            )
        elif isinstance(credentials, TokenCredentials):
            self.client = self.get_hvac_client_from_token(
                url, credentials, hvac_adapter, hvac_client_verify
            )
        else:
            raise RuntimeError(
                "Please give a vault client or credentials as VaultSecret or VaultToken"
            )

        if not self.client.is_authenticated():
            raise RuntimeError("Vault Client not authenticated.")
        else:
            logging.debug("Vault client initialized")

    @staticmethod
    def get_hvac_client_from_secret(
        url: str,
        credentials: SecretCredentials,
        hvac_adapter: type[hvac.adapters.Adapter],
        hvac_client_verify: bool,
    ):
        client = hvac.Client(
            url=url,
            verify=hvac_client_verify,
            adapter=hvac_adapter,
            kwargs={
                "role_id": credentials.role_id,
                "secret_id": credentials.secret_id,
            },
        )
        client.auth.approle.login(
            role_id=credentials.role_id,
            secret_id=credentials.secret_id,
        )
        return client

    @staticmethod
    def get_hvac_client_from_token(
        url: str,
        credentials: TokenCredentials,
        hvac_adapter: type[hvac.adapters.Adapter],
        hvac_client_verify: bool,
    ):
        client = hvac.Client(
            url=url,
            token=credentials.token,
            verify=hvac_client_verify,
            adapter=hvac_adapter,
        )

        if client.sys.is_sealed():
            client.sys.submit_unseal_key(credentials.unseal_key)

        return client

    def get_secrets(self, vault_key: str) -> dict:
        return self.client.secrets.kv.v2.read_secret(
            path=vault_key, mount_point=self.secret_mount
        )["data"]["data"]

    def update_secrets(self, vault_key: str, secret_data: dict):
        self.client.secrets.kv.v2.create_or_update_secret(
            path=vault_key,
            secret=secret_data,
            mount_point=self.secret_mount,
        )

    def delete_secrets(self, vault_key: str):
        self.client.secrets.kv.v2.delete_metadata_and_all_versions(
            path=vault_key,
            mount_point=self.secret_mount,
        )
