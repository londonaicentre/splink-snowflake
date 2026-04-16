import os
import time

import pytest
import snowflake.connector
from snowflake.connector import SnowflakeConnection

from splink_snowflake import SnowflakeAPI

DATABASE = "SPLINK_DEV"


@pytest.fixture(scope="session")
def snowflake_connection() -> SnowflakeConnection:
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        database=DATABASE,
        warehouse="COMPUTE_WH",
        authenticator=os.environ.get("SNOWFLAKE_AUTHENTICATOR", "snowflake"),
        token=os.environ.get("SNOWFLAKE_TOKEN"),
        workload_identity_provider=os.environ.get(
            "SNOWFLAKE_WORKLOAD_IDENTITY_PROVIDER"
        ),
    )


@pytest.fixture(scope="session", autouse=True)
def test_schema(snowflake_connection: SnowflakeConnection):
    schema = f"TEST_RUN_{int(time.time())}"
    snowflake_connection.cursor().execute("USE ROLE SYSADMIN;")
    snowflake_connection.cursor().execute("USE WAREHOUSE COMPUTE_WH;")
    snowflake_connection.cursor().execute(f"CREATE SCHEMA {DATABASE}.{schema}")
    snowflake_connection.cursor().execute(f"USE SCHEMA {schema}")
    yield schema
    snowflake_connection.cursor().execute(
        f"DROP SCHEMA IF EXISTS {DATABASE}.{schema} CASCADE"
    )


@pytest.fixture(scope="function")
def snowflake_api(snowflake_connection: SnowflakeConnection) -> SnowflakeAPI:
    return SnowflakeAPI(connection=snowflake_connection)


"""
-- setup_splink_dev.sql
-- For running on temporary development accounts: not recommended to alter production
-- accounts with the following security policies.

USE ROLE ACCOUNTADMIN;

CREATE DATABASE IF NOT EXISTS CONTROL;
CREATE SCHEMA IF NOT EXISTS AUTHENTICATION_POLICIES;

CREATE OR REPLACE AUTHENTICATION POLICY CONTROL.AUTHENTICATION_POLICIES.AUTH_POL_SPLINK_DEV
  PAT_POLICY = (
    NETWORK_POLICY_EVALUATION = NOT_ENFORCED
  );

CREATE SCHEMA IF NOT EXISTS NETWORK_POLICIES;

CREATE OR REPLACE NETWORK RULE CONTROL.NETWORK_POLICIES.PAT_ALLOW_ALL_RULE
  MODE = INGRESS
  TYPE = IPV4
  VALUE_LIST = ('0.0.0.0/0');

CREATE OR REPLACE NETWORK POLICY NET_POL_ALLOW_ALL
  ALLOWED_NETWORK_RULE_LIST = ('CONTROL.NETWORK_POLICIES.PAT_ALLOW_ALL_RULE');

ALTER ACCOUNT SET NETWORK_POLICY = 'NET_POL_ALLOW_ALL';

-- Create Splink Dev Database with ownership to SYSADMIN

USE ROLE SYSADMIN;

CREATE DATABASE IF NOT EXISTS SPLINK_DEV;

ALTER USER REMOVE PROGRAMMATIC ACCESS TOKEN SPLINK_DEV_PAT;

ALTER USER ADD PROGRAMMATIC ACCESS TOKEN SPLINK_DEV_PAT
  DAYS_TO_EXPIRY = 30
  COMMENT = 'PAT for Splink Dev'
->>
SELECT
  '[connections.splink_dev]' || '\n' ||
  'account = "' || CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME() || '"\n' ||
  'user = "' || CURRENT_USER() || '"\n' ||
  'password = "' || "token_secret" || '"\n' ||
  'role = "SYSADMIN"' || '\n' ||
  'warehouse = "COMPUTE_WH"' || '\n' ||
  'database = "SPLINK_DEV"' || '\n' ||
  'schema = "PUBLIC"'
  AS connection_config
FROM $1;

-- To clean up PAT:
-- ALTER USER REMOVE PROGRAMMATIC ACCESS TOKEN SPLINK_DEV_PAT;
"""
