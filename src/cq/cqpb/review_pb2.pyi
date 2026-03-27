import datetime

from cq.v1 import knowledge_unit_pb2 as _knowledge_unit_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReviewStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REVIEW_STATUS_UNSPECIFIED: _ClassVar[ReviewStatus]
    REVIEW_STATUS_PENDING: _ClassVar[ReviewStatus]
    REVIEW_STATUS_APPROVED: _ClassVar[ReviewStatus]
    REVIEW_STATUS_REJECTED: _ClassVar[ReviewStatus]
REVIEW_STATUS_UNSPECIFIED: ReviewStatus
REVIEW_STATUS_PENDING: ReviewStatus
REVIEW_STATUS_APPROVED: ReviewStatus
REVIEW_STATUS_REJECTED: ReviewStatus

class ReviewItem(_message.Message):
    __slots__ = ("knowledge_unit", "status", "reviewed_by", "reviewed_at")
    KNOWLEDGE_UNIT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REVIEWED_BY_FIELD_NUMBER: _ClassVar[int]
    REVIEWED_AT_FIELD_NUMBER: _ClassVar[int]
    knowledge_unit: _knowledge_unit_pb2.KnowledgeUnit
    status: ReviewStatus
    reviewed_by: str
    reviewed_at: _timestamp_pb2.Timestamp
    def __init__(self, knowledge_unit: _Optional[_Union[_knowledge_unit_pb2.KnowledgeUnit, _Mapping]] = ..., status: _Optional[_Union[ReviewStatus, str]] = ..., reviewed_by: _Optional[str] = ..., reviewed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ReviewQueueResponse(_message.Message):
    __slots__ = ("items", "total", "offset", "limit")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[ReviewItem]
    total: int
    offset: int
    limit: int
    def __init__(self, items: _Optional[_Iterable[_Union[ReviewItem, _Mapping]]] = ..., total: _Optional[int] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class ReviewDecisionResponse(_message.Message):
    __slots__ = ("unit_id", "status", "reviewed_by", "reviewed_at")
    UNIT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REVIEWED_BY_FIELD_NUMBER: _ClassVar[int]
    REVIEWED_AT_FIELD_NUMBER: _ClassVar[int]
    unit_id: str
    status: ReviewStatus
    reviewed_by: str
    reviewed_at: _timestamp_pb2.Timestamp
    def __init__(self, unit_id: _Optional[str] = ..., status: _Optional[_Union[ReviewStatus, str]] = ..., reviewed_by: _Optional[str] = ..., reviewed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DailyCount(_message.Message):
    __slots__ = ("date", "proposed", "approved", "rejected")
    DATE_FIELD_NUMBER: _ClassVar[int]
    PROPOSED_FIELD_NUMBER: _ClassVar[int]
    APPROVED_FIELD_NUMBER: _ClassVar[int]
    REJECTED_FIELD_NUMBER: _ClassVar[int]
    date: _timestamp_pb2.Timestamp
    proposed: int
    approved: int
    rejected: int
    def __init__(self, date: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., proposed: _Optional[int] = ..., approved: _Optional[int] = ..., rejected: _Optional[int] = ...) -> None: ...

class TrendsResponse(_message.Message):
    __slots__ = ("daily",)
    DAILY_FIELD_NUMBER: _ClassVar[int]
    daily: _containers.RepeatedCompositeFieldContainer[DailyCount]
    def __init__(self, daily: _Optional[_Iterable[_Union[DailyCount, _Mapping]]] = ...) -> None: ...

class StatusCounts(_message.Message):
    __slots__ = ("pending", "approved", "rejected")
    PENDING_FIELD_NUMBER: _ClassVar[int]
    APPROVED_FIELD_NUMBER: _ClassVar[int]
    REJECTED_FIELD_NUMBER: _ClassVar[int]
    pending: int
    approved: int
    rejected: int
    def __init__(self, pending: _Optional[int] = ..., approved: _Optional[int] = ..., rejected: _Optional[int] = ...) -> None: ...

class ConfidenceBucket(_message.Message):
    __slots__ = ("lower", "upper", "count")
    LOWER_FIELD_NUMBER: _ClassVar[int]
    UPPER_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    lower: float
    upper: float
    count: int
    def __init__(self, lower: _Optional[float] = ..., upper: _Optional[float] = ..., count: _Optional[int] = ...) -> None: ...

class ReviewStatsResponse(_message.Message):
    __slots__ = ("counts", "domains", "confidence_distribution", "trends")
    class DomainsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    COUNTS_FIELD_NUMBER: _ClassVar[int]
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    TRENDS_FIELD_NUMBER: _ClassVar[int]
    counts: StatusCounts
    domains: _containers.ScalarMap[str, int]
    confidence_distribution: _containers.RepeatedCompositeFieldContainer[ConfidenceBucket]
    trends: TrendsResponse
    def __init__(self, counts: _Optional[_Union[StatusCounts, _Mapping]] = ..., domains: _Optional[_Mapping[str, int]] = ..., confidence_distribution: _Optional[_Iterable[_Union[ConfidenceBucket, _Mapping]]] = ..., trends: _Optional[_Union[TrendsResponse, _Mapping]] = ...) -> None: ...
