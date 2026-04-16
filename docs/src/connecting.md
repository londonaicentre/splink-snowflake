# Connecting to Snowflake

`splink-snowflake` accepts any `snowflake.connector.SnowflakeConnection`. How you obtain that connection is up to you.

## Local development

The simplest approach locally is to configure a named connection in `~/.snowflake/connections.toml` and use `SnowflakeConnection()`, which reads the default connection (overridable with the `SNOWFLAKE_DEFAULT_CONNECTION_NAME` environment variable):

```python
from snowflake.connector import SnowflakeConnection
import snowflake.connector

conn = SnowflakeConnection()
```

Named connections in `~/.snowflake/connections.toml` look like:

```toml
[connections.my_connection]
account = "myorg-myaccount"
user = "my_user"
password = "..."
database = "SPLINK_DEV"
warehouse = "COMPUTE_WH"
role = "SYSADMIN"
```

## CI / GitHub Actions (OIDC)

For CI, use `snowflake.connector.connect()` with explicit parameters. When authenticating with Workload Identity (OIDC via GitHub Actions), the relevant environment variables are set automatically by the [`snowflake-cli-action`](https://github.com/snowflakedb/snowflake-cli-action):

| Environment variable | Description |
|---|---|
| `SNOWFLAKE_ACCOUNT` | Snowflake account identifier |
| `SNOWFLAKE_AUTHENTICATOR` | Set to `WORKLOAD_IDENTITY` |
| `SNOWFLAKE_WORKLOAD_IDENTITY_PROVIDER` | Set to `OIDC` |
| `SNOWFLAKE_TOKEN` | The OIDC token |

```python
import os
import snowflake.connector

conn = snowflake.connector.connect(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    database="SPLINK_DEV",
    warehouse="COMPUTE_WH",
    authenticator=os.environ.get("SNOWFLAKE_AUTHENTICATOR", "snowflake"),
    token=os.environ.get("SNOWFLAKE_TOKEN"),
    workload_identity_provider=os.environ.get("SNOWFLAKE_WORKLOAD_IDENTITY_PROVIDER"),
)
```

See the [Snowflake OIDC documentation](https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/configure-connections#use-a-temporary-connection) for setup instructions on the Snowflake side.
