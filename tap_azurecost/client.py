"""REST client handling, including azureCostManagementStream base class."""

from __future__ import annotations

import typing as t
from functools import cached_property
from importlib import resources

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream

from tap_azurecost.auth import azureCostManagementAuthenticator
from tap_azurecost.utils.acm_transform import merge_columns_and_rows

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Auth, Context


# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = resources.files(__package__) / "schemas"


class azureCostManagementStream(RESTStream):
    """azureCostManagement stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""

        subscription_id = self.config["subscription_id"]

        return f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/dataplatformfm-sandbox-dev-rg/providers/Microsoft.CostManagement"

    @cached_property
    def authenticator(self) -> Auth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return azureCostManagementAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance.
        """
        return super().get_new_paginator()

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    def prepare_request_payload(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ARG002, ANN401
    ) -> dict | None:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary with the JSON body for a POST requests.
        """

        type = self.config.get("type")
        timeframe = self.config.get("timeframe")
        dataset = self.config.get("dataset")

        data = {
            "type": type,
            "dataset": dataset
        }

        if (timeframe != None):
            data["timeframe"] = timeframe

        return data

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        properties = response.json().get("properties")

        return merge_columns_and_rows(properties)
