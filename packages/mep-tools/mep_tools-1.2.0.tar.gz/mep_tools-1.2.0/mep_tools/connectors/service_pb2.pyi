from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Service(_message.Message):
    __slots__ = ["key", "name", "created_at", "updated_at", "type", "icon", "editor_config"]
    class ServiceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        SERVICE_TYPE_UNSPECIFIED: _ClassVar[Service.ServiceType]
        SERVICE_TYPE_ATS: _ClassVar[Service.ServiceType]
        SERVICE_TYPE_CHANNEL: _ClassVar[Service.ServiceType]
        SERVICE_TYPE_PLATFORM: _ClassVar[Service.ServiceType]
    SERVICE_TYPE_UNSPECIFIED: Service.ServiceType
    SERVICE_TYPE_ATS: Service.ServiceType
    SERVICE_TYPE_CHANNEL: Service.ServiceType
    SERVICE_TYPE_PLATFORM: Service.ServiceType
    KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    EDITOR_CONFIG_FIELD_NUMBER: _ClassVar[int]
    key: str
    name: str
    created_at: str
    updated_at: str
    type: Service.ServiceType
    icon: str
    editor_config: _any_pb2.Any
    def __init__(self, key: _Optional[str] = ..., name: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., type: _Optional[_Union[Service.ServiceType, str]] = ..., icon: _Optional[str] = ..., editor_config: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class ServicesRequest(_message.Message):
    __slots__ = ["company_id"]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    company_id: str
    def __init__(self, company_id: _Optional[str] = ...) -> None: ...

class ServicesResponse(_message.Message):
    __slots__ = ["services"]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    services: _containers.RepeatedCompositeFieldContainer[Service]
    def __init__(self, services: _Optional[_Iterable[_Union[Service, _Mapping]]] = ...) -> None: ...

class ServiceRequest(_message.Message):
    __slots__ = ["company_id", "key"]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    company_id: str
    key: str
    def __init__(self, company_id: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class ServiceResponse(_message.Message):
    __slots__ = ["service"]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: Service
    def __init__(self, service: _Optional[_Union[Service, _Mapping]] = ...) -> None: ...
