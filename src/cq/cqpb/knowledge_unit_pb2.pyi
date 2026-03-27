import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Tier(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIER_UNSPECIFIED: _ClassVar[Tier]
    TIER_LOCAL: _ClassVar[Tier]
    TIER_PRIVATE: _ClassVar[Tier]
    TIER_PUBLIC: _ClassVar[Tier]

class FlagReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FLAG_REASON_UNSPECIFIED: _ClassVar[FlagReason]
    FLAG_REASON_STALE: _ClassVar[FlagReason]
    FLAG_REASON_INCORRECT: _ClassVar[FlagReason]
    FLAG_REASON_DUPLICATE: _ClassVar[FlagReason]
TIER_UNSPECIFIED: Tier
TIER_LOCAL: Tier
TIER_PRIVATE: Tier
TIER_PUBLIC: Tier
FLAG_REASON_UNSPECIFIED: FlagReason
FLAG_REASON_STALE: FlagReason
FLAG_REASON_INCORRECT: FlagReason
FLAG_REASON_DUPLICATE: FlagReason

class Flag(_message.Message):
    __slots__ = ("reason", "timestamp")
    REASON_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    reason: FlagReason
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, reason: _Optional[_Union[FlagReason, str]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Insight(_message.Message):
    __slots__ = ("summary", "detail", "action")
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    summary: str
    detail: str
    action: str
    def __init__(self, summary: _Optional[str] = ..., detail: _Optional[str] = ..., action: _Optional[str] = ...) -> None: ...

class Context(_message.Message):
    __slots__ = ("languages", "frameworks", "pattern")
    LANGUAGES_FIELD_NUMBER: _ClassVar[int]
    FRAMEWORKS_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    languages: _containers.RepeatedScalarFieldContainer[str]
    frameworks: _containers.RepeatedScalarFieldContainer[str]
    pattern: str
    def __init__(self, languages: _Optional[_Iterable[str]] = ..., frameworks: _Optional[_Iterable[str]] = ..., pattern: _Optional[str] = ...) -> None: ...

class Evidence(_message.Message):
    __slots__ = ("confidence", "confirmations", "first_observed", "last_confirmed")
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    CONFIRMATIONS_FIELD_NUMBER: _ClassVar[int]
    FIRST_OBSERVED_FIELD_NUMBER: _ClassVar[int]
    LAST_CONFIRMED_FIELD_NUMBER: _ClassVar[int]
    confidence: float
    confirmations: int
    first_observed: _timestamp_pb2.Timestamp
    last_confirmed: _timestamp_pb2.Timestamp
    def __init__(self, confidence: _Optional[float] = ..., confirmations: _Optional[int] = ..., first_observed: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_confirmed: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class KnowledgeUnit(_message.Message):
    __slots__ = ("id", "version", "domain", "insight", "context", "evidence", "tier", "created_by", "superseded_by", "flags")
    ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    INSIGHT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    EVIDENCE_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    SUPERSEDED_BY_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    version: int
    domain: _containers.RepeatedScalarFieldContainer[str]
    insight: Insight
    context: Context
    evidence: Evidence
    tier: Tier
    created_by: str
    superseded_by: str
    flags: _containers.RepeatedCompositeFieldContainer[Flag]
    def __init__(self, id: _Optional[str] = ..., version: _Optional[int] = ..., domain: _Optional[_Iterable[str]] = ..., insight: _Optional[_Union[Insight, _Mapping]] = ..., context: _Optional[_Union[Context, _Mapping]] = ..., evidence: _Optional[_Union[Evidence, _Mapping]] = ..., tier: _Optional[_Union[Tier, str]] = ..., created_by: _Optional[str] = ..., superseded_by: _Optional[str] = ..., flags: _Optional[_Iterable[_Union[Flag, _Mapping]]] = ...) -> None: ...
