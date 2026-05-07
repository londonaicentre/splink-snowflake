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
