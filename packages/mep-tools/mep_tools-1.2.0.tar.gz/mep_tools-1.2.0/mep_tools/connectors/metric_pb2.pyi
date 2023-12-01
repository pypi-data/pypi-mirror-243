from google.protobuf import any_pb2 as _any_pb2
import connector_pb2 as _connector_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Metric(_message.Message):
    __slots__ = ["key", "name", "created_at", "updated_at", "custom", "value_type", "config", "connector", "connected_metrics"]
    class ValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        VALUE_TYPE_UNKNOWN: _ClassVar[Metric.ValueType]
        VALUE_TYPE_INTEGER: _ClassVar[Metric.ValueType]
        VALUE_TYPE_FLOAT: _ClassVar[Metric.ValueType]
        VALUE_TYPE_STRING: _ClassVar[Metric.ValueType]
        VALUE_TYPE_DATE: _ClassVar[Metric.ValueType]
        VALUE_TYPE_BOOLEAN: _ClassVar[Metric.ValueType]
    VALUE_TYPE_UNKNOWN: Metric.ValueType
    VALUE_TYPE_INTEGER: Metric.ValueType
    VALUE_TYPE_FLOAT: Metric.ValueType
    VALUE_TYPE_STRING: Metric.ValueType
    VALUE_TYPE_DATE: Metric.ValueType
    VALUE_TYPE_BOOLEAN: Metric.ValueType
    KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_METRICS_FIELD_NUMBER: _ClassVar[int]
    key: str
    name: str
    created_at: str
    updated_at: str
    custom: bool
    value_type: Metric.ValueType
    config: _any_pb2.Any
    connector: _connector_pb2.Connector
    connected_metrics: _containers.RepeatedCompositeFieldContainer[Metric]
    def __init__(self, key: _Optional[str] = ..., name: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., custom: bool = ..., value_type: _Optional[_Union[Metric.ValueType, str]] = ..., config: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., connector: _Optional[_Union[_connector_pb2.Connector, _Mapping]] = ..., connected_metrics: _Optional[_Iterable[_Union[Metric, _Mapping]]] = ...) -> None: ...

class MetricsRequest(_message.Message):
    __slots__ = ["company_id", "connection"]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    company_id: str
    connection: str
    def __init__(self, company_id: _Optional[str] = ..., connection: _Optional[str] = ...) -> None: ...

class MetricsResponse(_message.Message):
    __slots__ = ["metrics"]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[Metric]
    def __init__(self, metrics: _Optional[_Iterable[_Union[Metric, _Mapping]]] = ...) -> None: ...

class MetricRequest(_message.Message):
    __slots__ = ["company_id", "key"]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    company_id: str
    key: str
    def __init__(self, company_id: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class MetricResponse(_message.Message):
    __slots__ = ["metric", "options"]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    metric: Metric
    options: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, metric: _Optional[_Union[Metric, _Mapping]] = ..., options: _Optional[_Iterable[str]] = ...) -> None: ...
