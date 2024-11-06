"""azureCostManagement tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_azurecost import streams


class TapazureCostManagement(Tap):
    """azureCostManagement tap class."""

    name = "tap-azurecost"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            secret=True,
            required=True,
            description="Client id for OAuth 2.0 authentication."
        ),
        th.Property(
            "client_secret",
            th.StringType,
            secret=True,
            required=True,
            description="Client secret id for OAuth 2.0 authentication."
        ),
        th.Property(
            "tenant_id",
            th.StringType,
            secret=True,
            required=True,
            description="Azure tenant id."
        ),
        th.Property(
            "subscription_id",
            th.StringType,
            secret=True,
            required=True,
            description="Azure subscription id."
        ),
        th.Property(
            "api_version",
            th.StringType,
            default='2023-11-01',
            required=True,
            description="API version."
        ),
        th.Property(
            "type",
            th.StringType,
            default="Usage",
            allowed_values=["Usage", "AmortizedCost", "ActualCost"],
            required=True,
            description="The type of the query."
        ),
        th.Property(
            "timeframe",
            th.StringType,
            allowed_values=["BillingMonthToDate", "Custom", "MonthToDate", "TheLastBillingMonth", "TheLastMonth", "WeekToDate"],
            description="The time frame for pulling data for the query"
        ),
        th.Property(
            "time_period",
            th.ObjectType(
                th.Property("from", th.StringType, description="The start date to pull data from.", required=True),
                th.Property("to", th.StringType, description="The end date to pull data to.", required=True)
            ),
            description="Has time period for pulling data for the query."
        ),
        th.Property(
            "dataset",
            th.ObjectType(
                th.Property("granularity", th.StringType, description="The granularity level of data."),
                th.Property(
                    "aggregation",
                    th.ObjectType(
                        additional_properties=th.ObjectType(
                            th.Property(
                                "name", 
                                th.StringType, 
                                description="The name of the aggregation function to use.", 
                                required=True
                            ),
                            th.Property(
                                "function", 
                                th.StringType, 
                                description="The name of the column to aggregate.", 
                                required=True,
                                allowed_values=["Sum"]
                            )
                        )
                    ),
                    description="Dictionary of aggregation expression to use in the query. The key of each item in the dictionary is the alias for the aggregated column. Query can have up to 2 aggregation clauses."
                ),
                th.Property(
                    "grouping",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property(
                                "type",
                                th.StringType,
                                description="The type of the column to group.",
                                required=True,
                                allowed_values=["Dimension", "TagKey"]
                            ),
                            th.Property(
                                "name", 
                                th.StringType, 
                                description="The name of the column to group.", 
                                required=True
                            )
                        ),
                    ),
                    description="Array of group by expression to use in the query. Query can have up to 2 group by clauses."
                ),
                th.Property(
                    "filter",
                    th.ObjectType(),
                    description="The filter expression to use in the query. Please reference our Query API REST documentation for how to properly format the filter."
                )
            ),
            required=True,
            description="Has definition for data in this query."
        )
    ).to_dict()

    def discover_streams(self) -> list[streams.azureCostManagementStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.QueryResultStream(self)
        ]

if __name__ == "__main__":
    TapazureCostManagement.cli()
