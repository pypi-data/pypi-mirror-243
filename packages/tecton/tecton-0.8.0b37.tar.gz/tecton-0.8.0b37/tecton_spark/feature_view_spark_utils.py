from pyspark.sql import DataFrame

from tecton_core import errors
from tecton_core.schema import Schema
from tecton_spark.schema_spark_utils import schema_from_spark


def validate_df_columns_and_feature_types(
    df: DataFrame, view_schema: Schema, allow_extraneous_columns: bool = True
) -> None:
    df_columns = frozenset(schema_from_spark(df.schema).column_name_and_data_types())
    df_column_names = frozenset([x[0] for x in df_columns])
    fv_columns = view_schema.column_name_and_data_types()
    fv_column_names = frozenset([x[0] for x in fv_columns])

    missing_columns = fv_column_names - df_column_names
    extraneous_columns = df_column_names - fv_column_names

    if missing_columns:
        raise errors.SCHEMA_VALIDATION_MISSING_COLUMNS_ERROR(list(missing_columns), list(fv_column_names))

    if not allow_extraneous_columns and extraneous_columns:
        raise errors.SCHEMA_VALIDATION_EXTRANEOUS_COLUMNS_ERROR(list(extraneous_columns), list(fv_column_names))

    for fv_column in fv_columns:
        if fv_column not in df_columns:
            raise errors.SCHEMA_VALIDATION_COLUMN_TYPE_MISMATCH_ERROR(
                fv_column[0], fv_column[1], [x for x in df_columns if x[0] == fv_column[0]][0][1]
            )
