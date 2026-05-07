# Changelog

## 0.1.2
### Added
- Implement Jaccard Similarity function name (using undocumented Snowflake function), and test

## 0.1.1
### Added
- Add OIDC / Workload Identity authentication support for GitHub Actions CI
- Add isolated test schema per run (`TEST_RUN_<epoch>`) with guaranteed teardown
- Add docs (this book)
- Initial PyPI release

## Fixed
- Fix bug which resulted in columns from tables with the same name outside the current session context (e.g. another schema) being added to a query: Force `INFORMATION_SCHEMA` to check only the current schema when inspecting tables.
  - This may constrain inspecting tables outside the current session context; will review in future releases.

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
