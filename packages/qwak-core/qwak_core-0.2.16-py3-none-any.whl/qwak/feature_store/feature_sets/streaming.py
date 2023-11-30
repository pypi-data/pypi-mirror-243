import functools
from dataclasses import dataclass
from typing import List, Optional

from _qwak_proto.qwak.feature_store.features.execution_pb2 import (
    StreamingExecutionSpec as ProtoStreamingExecutionSpec,
)
from _qwak_proto.qwak.feature_store.features.feature_set_pb2 import FeatureSetSpec
from _qwak_proto.qwak.feature_store.features.feature_set_types_pb2 import (
    FeatureSetType as ProtoFeatureSetType,
    StreamingFeatureSetV1 as ProtoStreamingFeatureSetV1,
)
from _qwak_proto.qwak.feature_store.sources.streaming_pb2 import (
    StreamingSource as ProtoStreamingSource,
)
from qwak.exceptions import QwakException
from qwak.feature_store._common.artifact_utils import ArtifactSpec
from qwak.feature_store.entities.entity import Entity
from qwak.feature_store.feature_sets.base_feature_set import BaseFeatureSet
from qwak.feature_store.feature_sets.execution_spec import ClusterTemplate
from qwak.feature_store.feature_sets.metadata import (
    Metadata,
    get_metadata_from_function,
    set_metadata_on_function,
)
from qwak.feature_store.feature_sets.transformations import StreamingTransformation
from typeguard import typechecked

_OFFLINE_SCHEDULING_ATTRIBUTE = "_qwak_offline_scheduling"
_OFFLINE_CLUSTER_SPEC = "_qwak_offline_cluster_specification"
_ONLINE_TRIGGER_INTERVAL = "_qwak_online_trigger_interval"
_ONLINE_CLUSTER_SPEC = "_qwak_online_cluster_specification"
_BACKFILL_SPEC = "_qwak_online_cluster_specification"
_METADATA_ = "_qwak_online_cluster_specification"


@typechecked
def feature_set(
    *,
    data_sources: List[str],
    timestamp_column_name: str,
    offline_scheduling_policy: Optional[str] = None,
    online_trigger_interval: Optional[int] = None,
    name: Optional[str] = None,
    entity: Optional[str] = None,
    key: Optional[str] = None,
):
    """
    Creates a streaming feature set for the specified entity using the given streaming data sources.

    A streaming feature set allows for real-time updates of features from live data sources, letting ML models access
    the most recent values without waiting for batch updates.

    :param entity: The name of the entity for which the feature set is being created. An entity typically represents a
                   unique object or concept, like 'user', 'product', etc. Entity and key are mutually exclusive.
    :param key: a column name in the feature set which is the key. Entity and key are mutually exclusive.
    :param data_sources: A list of references to the data sources from which the feature values will be streamed.
                                Each data source should be capable of providing data in a streaming manner.
    :param timestamp_column_name: The name of the column in the data source that contains timestamp information. This
                                  is used to order the data chronologically and ensure that the feature values are
                                  updated in the correct order.
    :param offline_scheduling_policy: Defines the offline ingestion policy - which affects the data freshness of
                                      the offline store. defaults to */30 * * * * (every 30 minutes)
    :param online_trigger_interval: Defines the online ingestion policy  - which affects the data freshness of
                                      the online store. defaults to 5 seconds
    :param name: An optional name for the feature set. If not provided, the name of the function will be used.

    Example:

    ... code-block:: python

        @streaming.feature_set(
            entity="users",
            data_sources=["users_registration_stream"],
            timestamp_column_name="reg_date"
        )
        def user_streaming_features():
            return SparkStreamingTransformation("SELECT user_id, reg_country, reg_date FROM data_source")
    """

    def decorator(function):
        user_transformation = function()
        if not isinstance(user_transformation, StreamingTransformation):
            raise ValueError(
                "Function must return a valid streaming transformation function"
            )
        if (not key) is (not entity):
            raise ValueError("Key or entity can be specified, not both")

        fs_name = name or function.__name__
        streaming_feature_set = StreamingFeatureSet(
            name=fs_name,
            entity=entity if entity else None,
            key=key if key else None,
            data_sources=data_sources,
            timestamp_column_name=timestamp_column_name,
            transformation=user_transformation,
            metadata=get_metadata_from_function(
                function, description=fs_name, display_name=fs_name
            ),
            online_trigger_interval=online_trigger_interval
            if online_trigger_interval
            else 5,
            offline_scheduling_policy=offline_scheduling_policy
            if offline_scheduling_policy
            else "*/30 * * * *",
            offline_cluster_template=getattr(
                function, _OFFLINE_CLUSTER_SPEC, ClusterTemplate.SMALL
            ),
            online_cluster_template=getattr(
                function, _ONLINE_CLUSTER_SPEC, ClusterTemplate.SMALL
            ),
        )

        functools.update_wrapper(streaming_feature_set, user_transformation)
        return streaming_feature_set

    return decorator


@typechecked
def execution_specification(
    *,
    online_cluster_template: Optional[ClusterTemplate] = None,
    offline_cluster_template: Optional[ClusterTemplate] = None,
):
    """
    Set the execution specification of the cluster running the feature set

    :param online_cluster_template: Predefined template sizes
    :param offline_cluster_template: Predefined template sizes

    Cluster template example:

    ... code-block:: python
        @streaming.feature_set(entity="users", data_sources=["streaming_users_source"])
        @streaming.execution_specification(
                offline_cluster_template=ClusterTemplate.MEDIUM,
                online_cluster_template=ClusterTemplate.MEDIUM)
        def user_streaming_features():
            return SparkStreamingTransformation("SELECT user_id, age, timestamp FROM streaming_users_source"
    """

    def decorator(user_transformation):
        setattr(user_transformation, _ONLINE_CLUSTER_SPEC, online_cluster_template)

        setattr(user_transformation, _OFFLINE_CLUSTER_SPEC, offline_cluster_template)

        return user_transformation

    return decorator


@typechecked
def metadata(
    *,
    owner: Optional[str] = None,
    description: Optional[str] = None,
    display_name: Optional[str] = None,
):
    """
    Sets additional user provided metadata

    :param owner: feature set owner
    :param description: General description of the feature set
    :param display_name: Human readable name of the feature set

    Example:

    ... code-block:: python

        @streaming.feature_set(
            entity="users",
            data_sources=["users_registration_stream"],
            timestamp_column_name="reg_date"
        )
        @streaming.metadata(
            owner="datainfra@qwak.com",
            display_name="User Streaming Features",
            description="Users feature from the Kafka topic of users registration stream",
        )
        def user_streaming_features():
            return SparkStreamingTransformation("SELECT user_id, reg_country, reg_date FROM data_source")

    """

    def decorator(user_transformation):
        _validate_decorator_ordering(user_transformation)
        set_metadata_on_function(user_transformation, owner, description, display_name)

        return user_transformation

    return decorator


def _validate_decorator_ordering(user_transformation):
    if isinstance(user_transformation, StreamingFeatureSet):
        raise ValueError(
            "Wrong decorator ordering - @streaming.feature_set should be the top most decorator"
        )


@dataclass
class StreamingFeatureSet(BaseFeatureSet):
    timestamp_column_name: str = None
    online_trigger_interval: int = None
    offline_scheduling_policy: str = None
    transformation: StreamingTransformation = None
    offline_cluster_template: ClusterTemplate = None
    online_cluster_template: ClusterTemplate = None
    metadata: Metadata = None

    @staticmethod
    def _from_proto(cls, proto: FeatureSetSpec):
        streaming_def = proto.feature_set_type.streaming_feature_set_v1

        return cls(
            name=proto.name,
            entity=Entity._from_proto(proto.entity),
            data_sources=[
                ds.data_source.name
                for ds in streaming_def.feature_set_streaming_sources
            ],
            timestamp_col_name=streaming_def.timestamp_column_name,
            online_trigger_interval=streaming_def.online_trigger_interval,
            offline_scheduling_policy=streaming_def.offline_scheduling_policy,
            transform=StreamingTransformation._from_proto(streaming_def.transformation),
            offline_cluster_template=streaming_def.execution_spec.offline_cluster_template,
            online_cluster_template=streaming_def.execution_spec.online_cluster_template,
            metadata=Metadata.from_proto(proto.metadata),
        )

    def _get_data_sources(self, feature_registry) -> List[ProtoStreamingSource]:
        sources: List[ProtoStreamingSource] = list()
        for name in self.data_sources:
            ds = feature_registry.get_data_source_by_name(name)
            if not ds:
                raise QwakException(f"Non-existent data source: {name}")
            else:
                sources.append(
                    ds.data_source.data_source_definition.data_source_spec.stream_source
                )
        return sources

    def _to_proto(
        self, git_commit, features, feature_registry, **kwargs
    ) -> FeatureSetSpec:
        data_sources = self._get_data_sources(feature_registry)

        return FeatureSetSpec(
            name=self.name,
            metadata=self.metadata.to_proto(),
            git_commit=git_commit,
            features=features,
            entity=self._get_entity_definition(feature_registry),
            feature_set_type=ProtoFeatureSetType(
                streaming_feature_set_v1=ProtoStreamingFeatureSetV1(
                    transformation=self.transformation._to_proto(),
                    data_sources=data_sources,
                    execution_spec=ProtoStreamingExecutionSpec(
                        online_cluster_template=ClusterTemplate.to_proto(
                            self.online_cluster_template
                        ),
                        offline_cluster_template=ClusterTemplate.to_proto(
                            self.offline_cluster_template
                        ),
                    ),
                    timestamp_column_name=self.timestamp_column_name,
                    online_trigger_interval=self.online_trigger_interval,
                    offline_scheduling_policy=self.offline_scheduling_policy,
                )
            ),
        )

    def _get_artifact_spec(self) -> Optional[ArtifactSpec]:
        return None
