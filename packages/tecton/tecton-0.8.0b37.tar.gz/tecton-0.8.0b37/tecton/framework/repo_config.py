"""Data models related to the Repo Config (i.e. the tecton.yaml file).

See PRD: https://www.notion.so/tecton/PRD-Repo-Config-725bd10a7ce6422eaedaf8786869ea35
"""
import logging
from typing import Optional

import pydantic
from typing_extensions import Annotated

from tecton.framework import configs
from tecton.framework.base_config import BaseTectonConfig


logger = logging.getLogger(__name__)


class RepoConfig(BaseTectonConfig):
    """The data model for the repo config (i.e. the tecton.yaml) file."""

    defaults: Optional["TectonObjectDefaults"] = None


def _number_to_string(value):
    if isinstance(value, (int, float)):
        return str(value)
    return value


# Users may attempt to provide a runtime version like '0.8', which could be parsed from yaml as a float instead of a
# string, which leads to unintuitive errors. This BeforeValidator will convert numbers to string.
TectonRuntimeVersionType = Annotated[str, pydantic.BeforeValidator(_number_to_string)]


class BatchFeatureViewDefaults(BaseTectonConfig):
    tecton_runtime_version: Optional[TectonRuntimeVersionType] = None
    # TODO(jake): The online store default is currently set at data proto creation time based on backend state. This
    # is a very fragile, inconsistent approach that we should reconsider.
    online_store: Optional[configs.OnlineStoreTypes] = pydantic.Field(default=None, discriminator="kind")
    offline_store: configs.OfflineStoreConfig = pydantic.Field(default_factory=configs.OfflineStoreConfig)
    batch_compute: configs.ComputeConfigTypes = pydantic.Field(
        default_factory=configs._DefaultClusterConfig, discriminator="kind"
    )


class StreamFeatureViewDefaults(BatchFeatureViewDefaults):
    stream_compute: configs.ComputeConfigTypes = pydantic.Field(
        default_factory=configs._DefaultClusterConfig, discriminator="kind"
    )


class FeatureTableDefaults(BatchFeatureViewDefaults):
    tecton_runtime_version: Optional[TectonRuntimeVersionType] = None

    # TODO(jake): The online store default is currently set at data proto creation time based on backend state. This
    # is a very fragile, inconsistent approach that we should reconsider.
    online_store: Optional[configs.OnlineStoreTypes] = pydantic.Field(default=None, discriminator="kind")
    offline_store: configs.OfflineStoreConfig = pydantic.Field(default_factory=configs.OfflineStoreConfig)


class FeatureServiceDefaults(BaseTectonConfig):
    on_demand_environment: Optional[str] = None


class TectonObjectDefaults(BaseTectonConfig):
    batch_feature_view: Optional[BatchFeatureViewDefaults] = None
    stream_feature_view: Optional[StreamFeatureViewDefaults] = None
    feature_table: Optional[FeatureTableDefaults] = None
    feature_service: Optional[FeatureServiceDefaults] = None


# Singleton Repo Config.
_repo_config: Optional[RepoConfig] = None


def set_repo_config(repo_config: RepoConfig) -> None:
    """Set the singleton instance of the repo config."""
    global _repo_config
    if _repo_config is not None:
        logger.warning("Overwriting Tecton repo config that was already set.")
    _repo_config = repo_config


def get_repo_config() -> Optional[RepoConfig]:
    """Get the singleton instance of the repo config. None if it has not been set.

    The repo config is expected to be None in non-plan/apply environments (e.g. notebooks) or if no config is found
    during plan/apply.
    """
    return _repo_config


def get_feature_service_defaults() -> FeatureServiceDefaults:
    """Get the user-specified Feature Service defaults or a default instance if the user did not specify defaults."""
    if _repo_config is None or _repo_config.defaults is None or _repo_config.defaults.feature_service is None:
        return FeatureServiceDefaults()

    return _repo_config.defaults.feature_service


def get_batch_feature_view_defaults() -> BatchFeatureViewDefaults:
    """Get the user-specified Batch FV defaults or a default instance if the user did not specify defaults."""
    if _repo_config is None or _repo_config.defaults is None or _repo_config.defaults.batch_feature_view is None:
        return BatchFeatureViewDefaults()

    return _repo_config.defaults.batch_feature_view


def get_stream_feature_view_defaults() -> StreamFeatureViewDefaults:
    """Get the user-specified Stream FV defaults or a default instance if the user did not specify defaults."""
    if _repo_config is None or _repo_config.defaults is None or _repo_config.defaults.stream_feature_view is None:
        return StreamFeatureViewDefaults()

    return _repo_config.defaults.stream_feature_view


def get_feature_table_defaults() -> FeatureTableDefaults:
    """Get the user-specified Feature Table defaults or a default instance if the user did not specify defaults."""
    if _repo_config is None or _repo_config.defaults is None or _repo_config.defaults.feature_table is None:
        return FeatureTableDefaults()

    return _repo_config.defaults.feature_table
