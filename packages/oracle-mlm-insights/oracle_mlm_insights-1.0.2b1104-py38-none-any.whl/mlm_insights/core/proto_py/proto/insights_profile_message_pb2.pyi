from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DatasetMetricMessage(_message.Message):
    __slots__ = ["dataset_metric_registry_messages"]
    DATASET_METRIC_REGISTRY_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    dataset_metric_registry_messages: MetricRegistryMessage
    def __init__(self, dataset_metric_registry_messages: _Optional[_Union[MetricRegistryMessage, _Mapping]] = ...) -> None: ...

class DatasetSummaryMessage(_message.Message):
    __slots__ = ["categorical_feature_count", "numerical_features_count", "total_features_count"]
    CATEGORICAL_FEATURE_COUNT_FIELD_NUMBER: _ClassVar[int]
    NUMERICAL_FEATURES_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FEATURES_COUNT_FIELD_NUMBER: _ClassVar[int]
    categorical_feature_count: int
    numerical_features_count: int
    total_features_count: int
    def __init__(self, total_features_count: _Optional[int] = ..., categorical_feature_count: _Optional[int] = ..., numerical_features_count: _Optional[int] = ...) -> None: ...

class FeatureMessage(_message.Message):
    __slots__ = ["column_type", "data_type", "metric_registry_messages", "name", "sfc_registry_messages", "variable_type"]
    COLUMN_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    METRIC_REGISTRY_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SFC_REGISTRY_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_TYPE_FIELD_NUMBER: _ClassVar[int]
    column_type: int
    data_type: str
    metric_registry_messages: MetricRegistryMessage
    name: str
    sfc_registry_messages: SFCRegistryMessage
    variable_type: int
    def __init__(self, name: _Optional[str] = ..., data_type: _Optional[str] = ..., variable_type: _Optional[int] = ..., metric_registry_messages: _Optional[_Union[MetricRegistryMessage, _Mapping]] = ..., sfc_registry_messages: _Optional[_Union[SFCRegistryMessage, _Mapping]] = ..., column_type: _Optional[int] = ...) -> None: ...

class MetricMessage(_message.Message):
    __slots__ = ["byte_serialized", "dataclass_param", "name"]
    BYTE_SERIALIZED_FIELD_NUMBER: _ClassVar[int]
    DATACLASS_PARAM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    byte_serialized: bytes
    dataclass_param: _struct_pb2.Struct
    name: str
    def __init__(self, name: _Optional[str] = ..., dataclass_param: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., byte_serialized: _Optional[bytes] = ...) -> None: ...

class MetricRegistryMessage(_message.Message):
    __slots__ = ["metric_map"]
    class MetricMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: MetricMessage
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[MetricMessage, _Mapping]] = ...) -> None: ...
    METRIC_MAP_FIELD_NUMBER: _ClassVar[int]
    metric_map: _containers.MessageMap[str, MetricMessage]
    def __init__(self, metric_map: _Optional[_Mapping[str, MetricMessage]] = ...) -> None: ...

class ProfileDatasetMessage(_message.Message):
    __slots__ = ["dataset_metric_message", "dataset_summary_message", "sdc_registry_message"]
    DATASET_METRIC_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DATASET_SUMMARY_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SDC_REGISTRY_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    dataset_metric_message: DatasetMetricMessage
    dataset_summary_message: DatasetSummaryMessage
    sdc_registry_message: SDCRegistryMessage
    def __init__(self, dataset_summary_message: _Optional[_Union[DatasetSummaryMessage, _Mapping]] = ..., dataset_metric_message: _Optional[_Union[DatasetMetricMessage, _Mapping]] = ..., sdc_registry_message: _Optional[_Union[SDCRegistryMessage, _Mapping]] = ...) -> None: ...

class ProfileFeatureMessage(_message.Message):
    __slots__ = ["feature_messages"]
    FEATURE_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    feature_messages: _containers.RepeatedCompositeFieldContainer[FeatureMessage]
    def __init__(self, feature_messages: _Optional[_Iterable[_Union[FeatureMessage, _Mapping]]] = ...) -> None: ...

class ProfileHeaderMessage(_message.Message):
    __slots__ = ["creation_timestamp", "daf_version", "tags", "version"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CREATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DAF_VERSION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    creation_timestamp: int
    daf_version: str
    tags: _containers.ScalarMap[str, str]
    version: str
    def __init__(self, version: _Optional[str] = ..., daf_version: _Optional[str] = ..., creation_timestamp: _Optional[int] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ProfileMessage(_message.Message):
    __slots__ = ["profile_data_message", "profile_feature_message", "profile_header_message"]
    PROFILE_DATA_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FEATURE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PROFILE_HEADER_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    profile_data_message: ProfileDatasetMessage
    profile_feature_message: ProfileFeatureMessage
    profile_header_message: ProfileHeaderMessage
    def __init__(self, profile_header_message: _Optional[_Union[ProfileHeaderMessage, _Mapping]] = ..., profile_data_message: _Optional[_Union[ProfileDatasetMessage, _Mapping]] = ..., profile_feature_message: _Optional[_Union[ProfileFeatureMessage, _Mapping]] = ...) -> None: ...

class SDCRegistryMessage(_message.Message):
    __slots__ = ["sdc_map"]
    class SdcMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ShareableDatasetComponentMessage
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ShareableDatasetComponentMessage, _Mapping]] = ...) -> None: ...
    SDC_MAP_FIELD_NUMBER: _ClassVar[int]
    sdc_map: _containers.MessageMap[str, ShareableDatasetComponentMessage]
    def __init__(self, sdc_map: _Optional[_Mapping[str, ShareableDatasetComponentMessage]] = ...) -> None: ...

class SFCRegistryMessage(_message.Message):
    __slots__ = ["sfc_map"]
    class SfcMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ShareableFeatureComponentMessage
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ShareableFeatureComponentMessage, _Mapping]] = ...) -> None: ...
    SFC_MAP_FIELD_NUMBER: _ClassVar[int]
    sfc_map: _containers.MessageMap[str, ShareableFeatureComponentMessage]
    def __init__(self, sfc_map: _Optional[_Mapping[str, ShareableFeatureComponentMessage]] = ...) -> None: ...

class ShareableDatasetComponentMessage(_message.Message):
    __slots__ = ["byte_serialized", "dataclass_param", "name"]
    BYTE_SERIALIZED_FIELD_NUMBER: _ClassVar[int]
    DATACLASS_PARAM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    byte_serialized: bytes
    dataclass_param: _struct_pb2.Struct
    name: str
    def __init__(self, name: _Optional[str] = ..., dataclass_param: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., byte_serialized: _Optional[bytes] = ...) -> None: ...

class ShareableFeatureComponentMessage(_message.Message):
    __slots__ = ["byte_serialized", "dataclass_param", "name"]
    BYTE_SERIALIZED_FIELD_NUMBER: _ClassVar[int]
    DATACLASS_PARAM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    byte_serialized: bytes
    dataclass_param: _struct_pb2.Struct
    name: str
    def __init__(self, name: _Optional[str] = ..., dataclass_param: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., byte_serialized: _Optional[bytes] = ...) -> None: ...
