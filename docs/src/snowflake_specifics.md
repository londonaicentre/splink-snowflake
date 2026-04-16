# Snowflake Specifics

## Identifier case

Snowflake uppercases unquoted identifiers by default. Splink generates quoted identifiers (e.g. `"first_name"`), which Snowflake treats as case-sensitive by default.

`SnowflakeAPI` sets `QUOTED_IDENTIFIERS_IGNORE_CASE = TRUE` on the session (controlled by `ignore_quoted_identifiers`), which makes Snowflake ignore case in quoted identifiers and avoids mismatches. If you disable this, ensure your column names are consistently cased.

Mixed-case table names will trigger a warning from `SnowflakeAPI`, as they are an anti-pattern under this setting.

## String similarity functions

Snowflake uses different function names from standard SQL for string similarity. The Snowflake dialect handles these translations automatically:

| Splink concept | Snowflake function |
|---|---|
| Levenshtein distance | `EDITDISTANCE` |
| Jaro-Winkler similarity | `JAROWINKLER_SIMILARITY` |
| Cosine similarity | `VECTOR_COSINE_SIMILARITY` |

When using comparison creators (e.g. `cl.LevenshteinAtThresholds`), the dialect translation is applied automatically. Avoid writing raw Levenshtein SQL in settings dicts — use comparison library functions instead.

## Transient tables

By default, intermediate Splink tables are created as `TRANSIENT` tables to avoid Time Travel storage overhead. These are automatically dropped at the end of a Splink run, so storage impact is minimal regardless.

## Sampling

Splink uses random sampling during `estimate_u_using_random_sampling`. On Snowflake this is implemented with `SAMPLE BERNOULLI(x%)`, with optional `REPEATABLE(seed)` for reproducibility.

## LOG2 UDF

Snowflake lacks a built-in `LOG2` function. `SnowflakeAPI` registers a temporary UDF at session start:

```sql
CREATE TEMPORARY FUNCTION IF NOT EXISTS LOG2(FLOAT_IN FLOAT)
RETURNS FLOAT AS $$ LOG(2, FLOAT_IN) $$;
```

This is scoped to the session and does not persist.
