# Contributing

## Setup

Clone the repo and install dependencies with [uv](https://github.com/astral-sh/uv):

```bash
git clone https://github.com/AICrossSectoral/splink-snowflake
cd splink-snowflake
uv sync
```

## Running tests

Integration tests run against a real Snowflake account. Configure a local connection named `splink_dev` in `~/.snowflake/connections.toml` (see [Connecting to Snowflake](./connecting.md)), then:

```bash
uv run pytest tests/
```

Tests create an isolated schema (`TEST_RUN_<epoch>`) in the `SPLINK_DEV` database and drop it on completion regardless of outcome.

### CI

Integration tests run on GitHub Actions against a Snowflake account using OIDC (Workload Identity) authentication. They are triggered on push to `main`, or on pull requests labelled `run-integration`.

## Snowflake account setup

The following SQL sets up the Snowflake side for development. Run as `ACCOUNTADMIN`:

```sql
USE ROLE ACCOUNTADMIN;

CREATE DATABASE IF NOT EXISTS CONTROL;

CREATE OR REPLACE AUTHENTICATION POLICY CONTROL.AUTHENTICATION_POLICIES.AUTH_POL_SPLINK_DEV
  PAT_POLICY = (NETWORK_POLICY_EVALUATION = NOT_ENFORCED);

CREATE OR REPLACE NETWORK RULE CONTROL.NETWORK_POLICIES.PAT_ALLOW_ALL_RULE
  MODE = INGRESS TYPE = IPV4
  VALUE_LIST = ('0.0.0.0/0');

CREATE OR REPLACE NETWORK POLICY NET_POL_ALLOW_ALL
  ALLOWED_NETWORK_RULE_LIST = ('CONTROL.NETWORK_POLICIES.PAT_ALLOW_ALL_RULE');

ALTER ACCOUNT SET NETWORK_POLICY = 'NET_POL_ALLOW_ALL';

USE ROLE SYSADMIN;

CREATE DATABASE IF NOT EXISTS SPLINK_DEV;
```
