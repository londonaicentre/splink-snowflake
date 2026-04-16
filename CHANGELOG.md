# Changelog

## Unreleased

- Add OIDC / Workload Identity authentication support for GitHub Actions CI
- Add isolated test schema per run (`TEST_RUN_<epoch>`) with guaranteed teardown
- Add docs (this book)

## 0.1.0

### Added

- Initial Snowflake backend implementation: `SnowflakeAPI`, `SnowflakeDataframe`, `SnowflakeDialect`
- `LOG2` UDF registered automatically at session start
- Transient table support for intermediate Splink tables
- `QUOTED_IDENTIFIERS_IGNORE_CASE` session setting for compatibility with Splink SQL generation
- Parquet and CSV export via `to_parquet` / `to_csv`
- Snowflake-specific string similarity mappings: `EDITDISTANCE`, `JAROWINKLER_SIMILARITY`, `VECTOR_COSINE_SIMILARITY`
- Bernoulli sampling with optional seed for `estimate_u_using_random_sampling`
- CI workflow with Snowflake integration tests
- PyPI release mechanism
