from splink_snowflake import SnowflakeAPI
from splink_snowflake.dialect import SnowflakeDialect
from snowflake.connector import SnowflakeConnection

from math import isclose


def test_jaccard_similarity(snowflake_connection: SnowflakeConnection):
    """
    Snowflake has an undocumented function `JACCARD_SIMILARITY(STRING, STRING)`.
    This test validates it exists.
    """
    # Implicitly calls _register_udfs
    cursor = snowflake_connection.cursor()
    # Have two checks
    result = cursor.execute(
        "SELECT JACCARD_SIMILARITY('DUCKY', 'LUCKY'), JACCARD_SIMILARITY('MARHTA', 'MARTHA');"
    )
    assert result
    res = result.fetchone()

    # Pass type check for not None
    assert res
    assert isclose(res[0], 0.6666666666666)
    assert res[1] == 1.0


def test_damerau_levenshtein(snowflake_api: SnowflakeAPI):
    """
    Test functionality creation and functioanlity of `DAMERAU_LEVENSHTEIN(STRING, STRING)`.
    """
    api = snowflake_api
    # Have two checks
    result = api._con.cursor().execute("SELECT DAMERAU_LEVENSHTEIN('CA', 'ABC')")
    assert result
    res = result.fetchone()

    # Pass type check for not None
    assert res
    assert res[0] == 2


def test_damerau_levenshtein_function_name_exists():
    # Implicit assertion no error raised
    try:
        SnowflakeDialect().damerau_levenshtein_function_name
    except Exception as exc:
        assert False, f"`damerau_levenshtein_function_name` raised an exception {exc}"

def test_jaro_function_exists():
    # Implicit assertion no error raised

    try:
        print(SnowflakeDialect().jaro_function_name)
    except Exception as exc:
        assert False, f"`jaro_function_name` raised an exception {exc}"
