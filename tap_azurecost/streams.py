"""Stream type classes for tap-azurecost."""

from __future__ import annotations

import typing as t
from importlib import resources

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_azurecost.client import azureCostManagementStream

class QueryResultStream(azureCostManagementStream):
    rest_method='POST'
    name="query_result"
    schema = th.PropertiesList()

    def __init__(self, tap):
        super().__init__(tap)

        self.path = f"/query?api-version={self.config['api_version']}"

        dataset = self.config.get("dataset")

        properties = [
            th.Property("UsageDate", th.NumberType),
            th.Property("Currency", th.StringType)
        ]

        if dataset != None:
            aggregation = dataset.get("aggregation")

            if aggregation != None:
                for key, value in aggregation.items():
                    name = value.get("name")

                    if name == None:
                        raise Exception("'aggregation' format is invalid.")
                    
                    properties.append(th.Property(name, th.NumberType))

            grouping = dataset.get("grouping")

            if grouping != None:
                for item in grouping:
                    type = item.get("type")
                    name = item.get("name")

                    if type == None or name == None:
                        raise Exception("'grouping' format is invalid.")

                    if type == "TagKey":
                        properties.append(th.Property("TagKey", th.StringType))
                        properties.append(th.Property("TagValue", th.StringType))
                    elif type == "Dimension":
                        properties.append(th.Property(name, th.StringType))

        self.schema = th.PropertiesList(*properties).to_dict()
                    
    