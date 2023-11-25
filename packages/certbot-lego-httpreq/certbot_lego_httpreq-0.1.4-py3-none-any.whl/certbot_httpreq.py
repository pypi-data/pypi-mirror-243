from typing import Any, Callable

from certbot import errors
from certbot.plugins import dns_common

import httpx


class _HTTPreqClient:
    def __init__(
        self, endpoint: str, username: str = None, password: str = None
    ) -> None:
        self.auth = (username, password) if (username and password) else None
        self.endpoint = endpoint

    def post(self, action: str, validation_name: str, validation_data: str) -> None:
        url = f"{self.endpoint}/{action}"
        if validation_name.endswith("."):
            fqdn = validation_name
        else:
            fqdn = f"{validation_name}."
        data = {
            "fqdn": fqdn,
            "value": validation_data,
        }
        resp = httpx.post(url, data=data, auth=self.auth)
        if resp.status_code != 200:
            raise errors.PluginError(f"Validation returned error {resp.text}.")

    def perform(self, validation_name: str, validation_data: str) -> None:
        self.post("present", validation_name, validation_data)

    def cleanup(self, validation_name: str, validation_data: str) -> None:
        self.post("cleanup", validation_name, validation_data)


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for HTTP Requests like lego uses

    This Authenticator sends a HTTP request to a custom endpoint to fulfill a dns-01 challenge
    """

    description = "HTTP Request authenticator"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def add_parser_arguments(
        cls,
        add: Callable[..., None],  # pylint: disable=arguments-differ
        default_propagation_seconds: int = 60,
    ) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add("credentials", help="HTTP Request credentials INI file")

    def more_info(self) -> str:
        return "This plugin configures a DNS TXT record to respond to a dns-01 challenge using a custom HTTP endpoint in the same way lego does."

    def _validate_credentials(
        self, credentials: dns_common.CredentialsConfiguration
    ) -> None:
        endpoint = credentials.conf("endpoint")
        username = credentials.conf("username")
        password = credentials.conf("password")

        if not endpoint:
            raise errors.PluginError(
                f"{credentials.confobj.filename} dns_httpreq_endpoint is required."
            )

        if username and not password:
            raise errors.PluginError(
                f"{credentials.confobj.filename} dns_httpreq_password must be provided when using a username"
            )
        if password and not username:
            raise errors.PluginError(
                f"{credentials.confobj.filename} dns_httpreq_username must be provided when using a password"
            )

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            "credentials",
            "HTTP Request credentials INI file",
            None,
            self._validate_credentials,
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_httpreq_client().perform(validation_name, validation)

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_httpreq_client().cleanup(validation_name, validation)

    def _get_httpreq_client(self) -> _HTTPreqClient:
        if not self.credentials:
            raise errors.Error("Plugin has not been prepared.")
        return _HTTPreqClient(
            self.credentials.conf("endpoint"),
            self.credentials.conf("username"),
            self.credentials.conf("password"),
        )
