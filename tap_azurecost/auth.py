"""azureCostManagement Authentication."""

from __future__ import annotations

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class azureCostManagementAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for azureCostManagement."""

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the AutomaticTestTap API.

        Returns:
            A dict with the request body
        """
        
        return {
            "scope": "https://management.azure.com/.default",
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "grant_type": "client_credentials",
        }

    @classmethod
    def create_for_stream(cls, stream) -> azureCostManagementAuthenticator:  # noqa: ANN001
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new authenticator.
        """
        return cls(
            stream=stream,
            auth_endpoint=f"https://login.microsoftonline.com/{stream.config["tenant_id"]}/oauth2/v2.0/token",
            oauth_scopes=["https://management.azure.com/.default"],
        )
