from google.protobuf import any_pb2 as _any_pb2
import service_pb2 as _service_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Connector(_message.Message):
    __slots__ = ["key", "name", "created_at", "updated_at", "service", "config"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    key: str
    name: str
    created_at: str
    updated_at: str
    service: _service_pb2.Service
    config: _any_pb2.Any
    def __init__(self, key: _Optional[str] = ..., name: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., service: _Optional[_Union[_service_pb2.Service, _Mapping]] = ..., config: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class DispatcherRequest(_message.Message):
    __slots__ = ["payload"]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: str
    def __init__(self, payload: _Optional[str] = ...) -> None: ...

class DispatcherResponse(_message.Message):
    __slots__ = ["payload"]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: str
    def __init__(self, payload: _Optional[str] = ...) -> None: ...

class ConnectorsRequest(_message.Message):
    __slots__ = ["company_id"]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    company_id: str
    def __init__(self, company_id: _Optional[str] = ...) -> None: ...

class ConnectorsResponse(_message.Message):
    __slots__ = ["connectors"]
    CONNECTORS_FIELD_NUMBER: _ClassVar[int]
    connectors: _containers.RepeatedCompositeFieldContainer[Connector]
    def __init__(self, connectors: _Optional[_Iterable[_Union[Connector, _Mapping]]] = ...) -> None: ...

class ConnectorRequest(_message.Message):
    __slots__ = ["company_id", "key"]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    company_id: str
    key: str
    def __init__(self, company_id: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class ConnectorResponse(_message.Message):
    __slots__ = ["connectors"]
    CONNECTORS_FIELD_NUMBER: _ClassVar[int]
    connectors: Connector
    def __init__(self, connectors: _Optional[_Union[Connector, _Mapping]] = ...) -> None: ...
