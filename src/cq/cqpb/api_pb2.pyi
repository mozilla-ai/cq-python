from cq.v1 import knowledge_unit_pb2 as _knowledge_unit_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProposeRequest(_message.Message):
    __slots__ = ("domain", "insight", "context", "created_by")
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    INSIGHT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    domain: _containers.RepeatedScalarFieldContainer[str]
    insight: _knowledge_unit_pb2.Insight
    context: _knowledge_unit_pb2.Context
    created_by: str
    def __init__(self, domain: _Optional[_Iterable[str]] = ..., insight: _Optional[_Union[_knowledge_unit_pb2.Insight, _Mapping]] = ..., context: _Optional[_Union[_knowledge_unit_pb2.Context, _Mapping]] = ..., created_by: _Optional[str] = ...) -> None: ...

class ProposeResponse(_message.Message):
    __slots__ = ("knowledge_unit",)
    KNOWLEDGE_UNIT_FIELD_NUMBER: _ClassVar[int]
    knowledge_unit: _knowledge_unit_pb2.KnowledgeUnit
    def __init__(self, knowledge_unit: _Optional[_Union[_knowledge_unit_pb2.KnowledgeUnit, _Mapping]] = ...) -> None: ...

class QueryRequest(_message.Message):
    __slots__ = ("domain", "language", "framework", "limit")
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    FRAMEWORK_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    domain: _containers.RepeatedScalarFieldContainer[str]
    language: str
    framework: str
    limit: int
    def __init__(self, domain: _Optional[_Iterable[str]] = ..., language: _Optional[str] = ..., framework: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("units",)
    UNITS_FIELD_NUMBER: _ClassVar[int]
    units: _containers.RepeatedCompositeFieldContainer[_knowledge_unit_pb2.KnowledgeUnit]
    def __init__(self, units: _Optional[_Iterable[_Union[_knowledge_unit_pb2.KnowledgeUnit, _Mapping]]] = ...) -> None: ...

class ConfirmRequest(_message.Message):
    __slots__ = ("unit_id",)
    UNIT_ID_FIELD_NUMBER: _ClassVar[int]
    unit_id: str
    def __init__(self, unit_id: _Optional[str] = ...) -> None: ...

class ConfirmResponse(_message.Message):
    __slots__ = ("knowledge_unit",)
    KNOWLEDGE_UNIT_FIELD_NUMBER: _ClassVar[int]
    knowledge_unit: _knowledge_unit_pb2.KnowledgeUnit
    def __init__(self, knowledge_unit: _Optional[_Union[_knowledge_unit_pb2.KnowledgeUnit, _Mapping]] = ...) -> None: ...

class FlagRequest(_message.Message):
    __slots__ = ("unit_id", "reason")
    UNIT_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    unit_id: str
    reason: _knowledge_unit_pb2.FlagReason
    def __init__(self, unit_id: _Optional[str] = ..., reason: _Optional[_Union[_knowledge_unit_pb2.FlagReason, str]] = ...) -> None: ...

class FlagResponse(_message.Message):
    __slots__ = ("knowledge_unit",)
    KNOWLEDGE_UNIT_FIELD_NUMBER: _ClassVar[int]
    knowledge_unit: _knowledge_unit_pb2.KnowledgeUnit
    def __init__(self, knowledge_unit: _Optional[_Union[_knowledge_unit_pb2.KnowledgeUnit, _Mapping]] = ...) -> None: ...

class StatsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StatsResponse(_message.Message):
    __slots__ = ("total_units", "domains")
    class DomainsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    TOTAL_UNITS_FIELD_NUMBER: _ClassVar[int]
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    total_units: int
    domains: _containers.ScalarMap[str, int]
    def __init__(self, total_units: _Optional[int] = ..., domains: _Optional[_Mapping[str, int]] = ...) -> None: ...

class HealthRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HealthResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
