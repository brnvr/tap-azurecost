# tap-azurecost

`tap-azurecost` is a Meltano tap for querying data from Azure Cost Management API. The full documentation of the API endpoint can be found [here](https://learn.microsoft.com/en-us/rest/api/cost-management/query/usage?view=rest-cost-management-2023-11-01&tabs=HTTP). The tap has currently been tested for version `2023-11-01` of the API, and may not behave correctly for different versions.

## Configuration

### Accepted Config Options

| Setting | Type | Required | Default | Description |
|:--------|:--------:|:--------:|:-------:|:------------|
| client_id | string | True     | None    | Client id for OAuth 2.0 authentication. |
| client_secret | string | True     | None    | Client secret id for OAuth 2.0 authentication. |
| tenant_id | string | True     | None    | Azure tenant id. |
| subscription_id | string | True     | None    | Azure subscription id. |
| api_version | string | True     | 2023-11-01 | API version. |
| type | [ExportType](https://learn.microsoft.com/en-us/rest/api/cost-management/query/usage?view=rest-cost-management-2023-11-01&tabs=HTTP#exporttype) | True     | Usage   | The type of the query. |
| timeframe| [TimeframeType](https://learn.microsoft.com/en-us/rest/api/cost-management/query/usage?view=rest-cost-management-2023-11-01&tabs=HTTP#timeframetype)  | False    | None    | The time frame for pulling data for the query |
| time_period | [QueryTimePeriod](https://learn.microsoft.com/en-us/rest/api/cost-management/query/usage?view=rest-cost-management-2023-11-01&tabs=HTTP#querytimeperiod) | False    | None    | Has time period for pulling data for the query. |
| dataset | [QueryDataset](https://learn.microsoft.com/en-us/rest/api/cost-management/query/usage?view=rest-cost-management-2023-11-01&tabs=HTTP#querydataset) | True     | None    | Has definition for data in this query. |
| dataset.granularity | [GranularityType](https://learn.microsoft.com/en-us/rest/api/cost-management/query/usage?view=rest-cost-management-2023-11-01&tabs=HTTP#granularitytype)| False    | None    | The granularity level of data. |
| dataset.aggregation | <string, [QueryAggregation](https://learn.microsoft.com/en-us/rest/api/cost-management/query/usage?view=rest-cost-management-2023-11-01&tabs=HTTP#queryaggregation)> | False    | None    | Dictionary of aggregation expression to use in the query. The key of each item in the dictionary is the alias for the aggregated column. Query can have up to 2 aggregation clauses. |
| dataset.grouping | [QueryGrouping](https://learn.microsoft.com/en-us/rest/api/cost-management/query/usage?view=rest-cost-management-2023-11-01&tabs=HTTP#querygrouping)[] | False    | None    | Array of group by expression to use in the query. Query can have up to 2 group by clauses. |
| dataset.filter | [QueryFilter](https://learn.microsoft.com/en-us/rest/api/cost-management/query/usage?view=rest-cost-management-2023-11-01&tabs=HTTP#queryfilter) | False    | None    | The filter expression to use in the query. Please reference our Query API REST documentation for how to properly format the filter. |

A full list of supported settings and capabilities for this tap is available by running:

```bash
tap-azurecost --about
```

### Example of configuration

#### meltano.yml

```yml
 config:
      timeframe: MonthToDate
      dataset:
        granularity: Daily
        aggregation:
          totalCost:
            name: PreTaxCost
            function: Sum
          totalCostUSD:
            name: PreTaxCostUSD
            function: Sum
        grouping:
          - type: TagKey
            name: clustername
          - type: Dimension
            name: ResourceGroup
        filter:
          tags:
            name: clustername
            operator: In
            values:
              - dbt_ci
```

#### .env

```
TAP_AZURECOST_CLIENT_ID=SOMETCLIENTID
TAP_AZURECOST_CLIENT_SECRET=SOMECLIENTSECRET
TAP_AZURECOST_TENANT_ID=SOMEAZURETENANTID
TAP_AZURECOST_SUBSCRIPTION_ID=SOMEAZURESUBSCRIPTIONID
```

