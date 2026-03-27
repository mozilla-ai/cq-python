from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RelevanceWeights(_message.Message):
    __slots__ = ("domain_weight", "language_weight", "framework_weight")
    DOMAIN_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    FRAMEWORK_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    domain_weight: float
    language_weight: float
    framework_weight: float
    def __init__(self, domain_weight: _Optional[float] = ..., language_weight: _Optional[float] = ..., framework_weight: _Optional[float] = ...) -> None: ...

class ConfidenceConstants(_message.Message):
    __slots__ = ("initial_confidence", "confirmation_boost", "flag_penalty", "ceiling", "floor")
    INITIAL_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    CONFIRMATION_BOOST_FIELD_NUMBER: _ClassVar[int]
    FLAG_PENALTY_FIELD_NUMBER: _ClassVar[int]
    CEILING_FIELD_NUMBER: _ClassVar[int]
    FLOOR_FIELD_NUMBER: _ClassVar[int]
    initial_confidence: float
    confirmation_boost: float
    flag_penalty: float
    ceiling: float
    floor: float
    def __init__(self, initial_confidence: _Optional[float] = ..., confirmation_boost: _Optional[float] = ..., flag_penalty: _Optional[float] = ..., ceiling: _Optional[float] = ..., floor: _Optional[float] = ...) -> None: ...
