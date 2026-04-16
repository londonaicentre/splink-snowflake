# Getting Started

Once you have a connection (see [Connecting to Snowflake](./connecting.md)), pass it to `SnowflakeAPI` and use it as the `db_api` argument to Splink's `Linker`:

```python
import pandas as pd
from snowflake.connector import SnowflakeConnection
from splink import Linker, SettingsCreator, block_on
import splink.comparison_library as cl

from splink_snowflake import SnowflakeAPI

conn = SnowflakeConnection()
db_api = SnowflakeAPI(connection=conn)

df = pd.read_csv("my_data.csv")

settings = SettingsCreator(
    link_type="dedupe_only",
    comparisons=[
        cl.LevenshteinAtThresholds("first_name", 2),
        cl.ExactMatch("surname"),
        cl.ExactMatch("dob"),
    ],
    blocking_rules_to_generate_predictions=[
        block_on("first_name", "surname"),
    ],
)

linker = Linker(df, settings, db_api=db_api)

linker.training.estimate_u_using_random_sampling(max_pairs=1e6)
df_predict = linker.inference.predict()
```

From here, refer to the [Splink documentation](https://moj-analytical-services.github.io/splink/) for the full API. Everything in Splink works the same way regardless of backend — `SnowflakeAPI` is a drop-in for `DuckDBAPI` or any other backend.
