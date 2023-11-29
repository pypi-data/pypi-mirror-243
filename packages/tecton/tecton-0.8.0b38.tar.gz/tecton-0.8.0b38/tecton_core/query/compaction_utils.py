import datetime
from collections import defaultdict
from typing import Optional
from typing import Tuple

import attrs

from tecton_core import feature_definition_wrapper
from tecton_core import schema
from tecton_core.specs import LifetimeWindowSpec
from tecton_core.specs import TimeWindowSpec
from tecton_core.specs import create_time_window_spec_from_data_proto
from tecton_proto.data import feature_view_pb2 as feature_view__data_pb2


@attrs.frozen
class AggregationGroup:
    """AggregationGroup represents a group of aggregate features to compute with a corresponding start/end.

    The typical usage of this will be in compaction jobs, where we will use the start/end time to determine
    eligible rows for each individual aggregate.
    """

    window_index: int
    inclusive_start_time: Optional[datetime.datetime]
    exclusive_end_time: datetime.datetime
    aggregate_features: Tuple[feature_view__data_pb2.AggregateFeature, ...]
    schema: schema.Schema


def _get_inclusive_start_time_for_window(
    exclusive_end_time: datetime.datetime, window: TimeWindowSpec
) -> Optional[datetime.datetime]:
    if isinstance(window, LifetimeWindowSpec):
        return None
    return exclusive_end_time + window.window_start


def _get_exclusive_end_time_for_window(
    exclusive_end_time: datetime.datetime, window: TimeWindowSpec
) -> datetime.datetime:
    if isinstance(window, LifetimeWindowSpec):
        return exclusive_end_time
    return exclusive_end_time + window.window_end


def aggregation_groups(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper, exclusive_end_time: datetime.datetime
) -> Tuple[AggregationGroup, ...]:
    aggregation_map = defaultdict(list)
    for aggregation in fdw.trailing_time_window_aggregation.features:
        aggregation_map[create_time_window_spec_from_data_proto(aggregation.time_window)].append(aggregation)

    agg_groups = fdw.fv_spec.online_batch_table_format.online_batch_table_parts

    if len(agg_groups) != len(aggregation_map):
        msg = "unexpected difference in length of the spec's online_batch_table_format and trailing_time_window_aggregation"
        raise ValueError(msg)

    return tuple(
        AggregationGroup(
            window_index=group.window_index,
            inclusive_start_time=_get_inclusive_start_time_for_window(exclusive_end_time, group.time_window),
            exclusive_end_time=_get_exclusive_end_time_for_window(exclusive_end_time, group.time_window),
            aggregate_features=tuple(aggregation_map[group.time_window]),
            schema=group.schema,
        )
        for group in agg_groups
    )
