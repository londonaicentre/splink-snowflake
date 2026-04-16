# splink-snowflake

Snowflake backend support for [Splink](https://moj-analytical-services.github.io/splink/), the data linkage and deduplication library.

> **Warning:** This backend is early stage and not fully stable. Maintenance is done on a best-effort basis and is not officially supported by the Splink team.

## What is this?

Splink supports multiple SQL backends (DuckDB, Spark, Athena, etc.). This package adds Snowflake to that list, letting you run Splink's probabilistic record linkage pipelines directly against data in Snowflake — without moving it out first.

## What is Splink?

Splink is a Python library for probabilistic record linkage and deduplication at scale. It uses an expectation-maximisation algorithm to estimate match weights, and generates SQL that runs natively against your chosen backend.

See the [Splink documentation](https://moj-analytical-services.github.io/splink/) for a full introduction to the concepts.
