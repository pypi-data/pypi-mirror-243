from enum import Enum

from tecton_core import conf
from tecton_core.query.dialect import Dialect
from tecton_proto.common import compute_mode_pb2


class ComputeMode(str, Enum):
    """Represents the compute mode for training data generation queries."""

    SPARK = "spark"
    SNOWFLAKE = "snowflake"
    ATHENA = "athena"
    RIFT = "rift"

    def default_dialect(self) -> Dialect:
        return _COMPUTE_MODE_TO_DIALECT[self]


_COMPUTE_MODE_TO_DIALECT = {
    ComputeMode.SPARK: Dialect.SPARK,
    ComputeMode.SNOWFLAKE: Dialect.SNOWFLAKE,
    ComputeMode.ATHENA: Dialect.ATHENA,
    ComputeMode.RIFT: Dialect.DUCKDB,
}


def get_compute_mode() -> ComputeMode:
    """Returns the default ComputeMode based on the environment."""
    offline_retrieval_mode = conf.get_or_none("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE")
    if offline_retrieval_mode is not None:
        try:
            offline_retrieval_mode = offline_retrieval_mode.lower()
            return ComputeMode(offline_retrieval_mode)
        except ValueError:
            msg = f"Invalid compute mode: {offline_retrieval_mode}. Must be one of: {', '.join(e.value for e in ComputeMode)}"
            raise ValueError(msg)
    else:
        # TODO(meastham): Delete me after #16346 is released and we're confident it won't roll back
        compute_mode = conf.get_or_raise("TECTON_COMPUTE_MODE")
        if compute_mode == ComputeMode.RIFT:
            return ComputeMode.RIFT
        elif conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED") or compute_mode == ComputeMode.SNOWFLAKE:
            return ComputeMode.SNOWFLAKE
        elif conf.get_bool("ALPHA_ATHENA_COMPUTE_ENABLED") or compute_mode == ComputeMode.ATHENA:
            return ComputeMode.ATHENA
        elif compute_mode == ComputeMode.SPARK:
            return ComputeMode.SPARK
        else:
            msg = f"Invalid Tecton compute mode: {compute_mode}. Must be one of {[[e.value for e in ComputeMode]]}"
            raise ValueError(msg)


class BatchComputeMode(Enum):
    """Represents that compute mode for batch jobs associated with a FeatureView."""

    SPARK = compute_mode_pb2.BatchComputeMode.BATCH_COMPUTE_MODE_SPARK
    SNOWFLAKE = compute_mode_pb2.BatchComputeMode.BATCH_COMPUTE_MODE_SNOWFLAKE
    RIFT = compute_mode_pb2.BatchComputeMode.BATCH_COMPUTE_MODE_RIFT

    @property
    def value(self) -> compute_mode_pb2.BatchComputeMode:
        return super().value


_COMPUTE_MODE_TO_BATCH = {
    ComputeMode.SPARK: BatchComputeMode.SPARK,
    ComputeMode.SNOWFLAKE: BatchComputeMode.SNOWFLAKE,
    ComputeMode.RIFT: BatchComputeMode.RIFT,
}

_STR_TO_BATCH = {
    "spark": BatchComputeMode.SPARK,
    "snowflake": BatchComputeMode.SNOWFLAKE,
    "rift": BatchComputeMode.RIFT,
}


def default_batch_compute_mode() -> BatchComputeMode:
    compute_mode = conf.get_or_none("TECTON_BATCH_COMPUTE_MODE")
    if compute_mode is not None:
        return _STR_TO_BATCH[compute_mode.lower()]
    else:
        # TODO(meastham): Delete me after #16346 is released and we're confident it won't roll back
        return _COMPUTE_MODE_TO_BATCH[get_compute_mode()]
