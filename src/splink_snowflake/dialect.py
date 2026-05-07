from splink.internals.comparison_level_library import ArrayIntersectLevel
from splink.internals.dialects import SplinkDialect


class SnowflakeDialect(SplinkDialect):
    _dialect_name_for_factory = "snowflake"

    @property
    def sql_dialect_str(self) -> str:  # pyright: ignore[reportIncompatibleMethodOverride]
        return "snowflake"

    @property
    def levenshtein_function_name(self) -> str:
        return "EDITDISTANCE"

    @property
    def jaro_winkler_function_name(self) -> str:
        return "JAROWINKLER_SIMILARITY"

    @property
    def jaccard_function_name(self) -> str:
        return "JACCARD_SIMILARITY"

    @property
    def cosine_similarity_function_name(self) -> str:
        return "VECTOR_COSINE_SIMILARITY"

    @property
    def array_max_function_name(self) -> str:
        return "ARRAY_MAX"

    @property
    def array_min_function_name(self) -> str:
        return "ARRAY_MIN"

    @property
    def array_transform_function_name(self) -> str:
        return "TRANSFORM"

    @property
    def array_first_index(self) -> int:
        return 0

    @property
    def greatest_function_name(self) -> str:
        return "GREATEST"

    @property
    def least_function_name(self) -> str:
        return "LEAST"

    def random_sample_sql(
        self, proportion, sample_size, seed=None, table=None, unique_id=None
    ):
        if proportion == 1.0:
            return ""
        percent = proportion * 100
        if seed:
            return f"SAMPLE BERNOULLI({percent}) REPEATABLE({seed})"
        else:
            return f"SAMPLE BERNOULLI({percent})"

    def _regex_extract_raw(
        self, name: str, pattern: str, capture_group: int = 0
    ) -> str:
        return f"REGEXP_SUBSTR({name}, '{pattern}', {capture_group + 1})"

    @property
    def default_timestamp_format(self):
        return "YYYY-MM-DD HH24:MI:SS.FF3"

    @property
    def default_date_format(self):
        return "YYYY-MM-DD"

    def try_parse_date(self, name: str, date_format: str | None = None) -> str:
        if date_format is None:
            date_format = self.default_date_format
        return f"""TRY_TO_DATE({name}, '{date_format}')"""

    def try_parse_timestamp(
        self, name: str, timestamp_format: str | None = None
    ) -> str:
        if timestamp_format is None:
            timestamp_format = self.default_timestamp_format
        return f"""TRY_TO_TIMESTAMP({name}, '{timestamp_format}')"""

    @property
    def infinity_expression(self):
        return "'inf'"

    def array_intersect(self, clc: ArrayIntersectLevel) -> str:
        """
        Snowflake override for array intersect SQL function
        """
        clc.col_expression.sql_dialect = self
        col = clc.col_expression
        thres = clc.min_intersection
        return f"ARRAY_SIZE(ARRAY_INTERSECTION({col.name_l}, {col.name_r})) >= {thres}"
