# Usage

## SnowflakeAPI

```python
from splink_snowflake import SnowflakeAPI

db_api = SnowflakeAPI(
    connection=conn,
    register_udfs=True,
    use_transient_tables=True,
    ignore_quoted_identifiers=True,
    query_tag="my_run__",
)
```

### Parameters

**`connection`** — A `snowflake.connector.SnowflakeConnection`. See [Connecting to Snowflake](./connecting.md).

**`register_udfs`** *(default: `True`)* — Registers a `LOG2` UDF as a temporary function in the session. Splink requires `LOG2` internally; Snowflake does not have a built-in `LOG2`, so this creates one automatically. Disable if you have already registered it yourself.

**`use_transient_tables`** *(default: `True`)* — Materialises intermediate Splink tables as `TRANSIENT` tables, which are excluded from Snowflake's Time Travel. This avoids unnecessary storage consumption for temporary computation. Set to `False` if you need Time Travel on intermediate results.

**`ignore_quoted_identifiers`** *(default: `True`)* — Sets `QUOTED_IDENTIFIERS_IGNORE_CASE = TRUE` on the session. This improves compatibility with Splink's SQL generation, which uses quoted identifiers. Disable if your schema relies on case-sensitive identifier behaviour.

**`query_tag`** *(default: timestamped string)* — Sets a Snowflake `QUERY_TAG` on the session, making it easier to identify Splink queries in query history. Set to `None` to disable.

## Accepted input types

`SnowflakeAPI` accepts the same input types as other Splink backends (pandas DataFrames, dicts, lists of dicts), plus `SnowflakeDataframe` — a lazy reference to a table already in Snowflake.

```python
from splink_snowflake import SnowflakeAPI

# Register a pandas DataFrame into Snowflake
db_api.register_table(df, "MY_TABLE")

# Or reference an existing Snowflake table directly
from splink_snowflake.dataframe import SnowflakeDataframe
sf_df = SnowflakeDataframe("MY_TABLE", "MY_TABLE", db_api)
```
