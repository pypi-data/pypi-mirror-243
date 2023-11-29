import datetime
import logging

import pendulum
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException

from tecton_core import specs
from tecton_core.fco_container import create_fco_container
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.id_helper import IdHelper
from tecton_core.offline_store import PartitionType
from tecton_materialization.batch_materialization import DEFAULT_COALESCE_FOR_S3
from tecton_proto.materialization.params_pb2 import MaterializationTaskParams
from tecton_spark.offline_store import DeltaWriter
from tecton_spark.offline_store import OfflineStoreWriterParams


logger = logging.getLogger(__name__)


def feature_export_from_params(spark: SparkSession, task_params: MaterializationTaskParams):
    export_params = task_params.feature_export_info.feature_export_parameters
    start_time = export_params.feature_start_time.ToDatetime()
    end_time = export_params.feature_end_time.ToDatetime()
    feature_view_id_str = IdHelper.to_string(task_params.feature_view.feature_view_id)
    parent_materialization_id_str = IdHelper.to_string(export_params.parent_materialization_task_id)

    logger.info(
        f"Starting feature export {task_params.materialization_task_id} job for feature view {feature_view_id_str}: parent_materialization_task_id: {parent_materialization_id_str} for time range {start_time} to {end_time}"
    )
    fco_container = create_fco_container(
        list(task_params.virtual_data_sources) + list(task_params.transformations) + list(task_params.entities),
        deserialize_funcs_to_main=True,
    )
    fv_spec = specs.create_feature_view_spec_from_data_proto(task_params.feature_view)

    # TODO (vitaly): move local import once tecton and materialization sdk is unified in all scenarios
    from tecton.framework.feature_view import feature_view_from_spec

    fd = FeatureDefinition(fv_spec, fco_container)
    fv = feature_view_from_spec(fv_spec, fco_container)

    tecton_df = fv.get_historical_features(start_time=start_time, end_time=end_time)
    try:
        spark_df = tecton_df.to_spark()
    except AnalysisException as e:
        if "Unable to infer schema for Parquet. It must be specified manually." in str(e):
            logger.warning("Unable to infer Parquet schema; assuming staging offline store is empty")
            return
        else:
            raise e
    if spark_df.rdd.isEmpty():
        logging.info(f"No features found for time range {start_time} to {end_time}")
        return

    spark.conf.set(
        "spark.databricks.delta.commitInfo.userMetadata",
        f'{{"featureStartTime":"{export_params.feature_start_time.ToJsonString()}", "featureEndTime": "{export_params.feature_end_time.ToJsonString()}"}}',
    )
    is_write_optimized = spark.conf.get("spark.databricks.delta.optimizeWrite.enabled", None) == "true"
    df_to_write = spark_df if is_write_optimized else spark_df.coalesce(DEFAULT_COALESCE_FOR_S3)

    table_location = export_params.export_store_path
    partition_size = datetime.timedelta(days=1)
    version = fd.get_feature_store_format_version
    logging.info(
        f"Writing features to {table_location} for time range {start_time} to {end_time} with partition size={partition_size}"
    )

    assert fd.timestamp_key is not None, "feature definition needs to have a timestamp key for feature export"

    export_store_params = OfflineStoreWriterParams(
        s3_path=table_location,
        always_store_anchor_column=True,
        time_column=fd.timestamp_key,
        join_key_columns=fd.join_keys,
        is_continuous=fd.is_continuous,
    )

    # TODO (vitaly): incorporate this into the offline_store.get_offline_store_writer factory
    # also use EPOCH as the partition type instead to save on timestamp conversions
    writer = DeltaWriter(export_store_params, spark, version, partition_size, PartitionType.DATE_STR)
    tile = pendulum.period(start_time, end_time)
    writer.overwrite_dataframe_in_tile(df_to_write, tile)
