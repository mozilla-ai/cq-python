"""Pydantic models for cq knowledge units."""

import uuid
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator

_KU_ID_PREFIX = "ku_"

# Legacy enum values written by pre-proto code (e.g. the MCP server plugin).
# Mapped to proto-canonical values on deserialization so the SDK always
# writes the correct format while remaining backwards-compatible with
# existing databases.
_LEGACY_TIER_MAP: dict[str, str] = {
    "local": "TIER_LOCAL",
    "team": "TIER_PRIVATE",
    "global": "TIER_PUBLIC",
}

_LEGACY_FLAG_REASON_MAP: dict[str, str] = {
    "stale": "FLAG_REASON_STALE",
    "incorrect": "FLAG_REASON_INCORRECT",
    "duplicate": "FLAG_REASON_DUPLICATE",
}


class Tier(StrEnum):
    """Knowledge unit storage tier."""

    UNSPECIFIED = "TIER_UNSPECIFIED"
    LOCAL = "TIER_LOCAL"
    PRIVATE = "TIER_PRIVATE"
    PUBLIC = "TIER_PUBLIC"


class FlagReason(StrEnum):
    """Reason for flagging a knowledge unit."""

    UNSPECIFIED = "FLAG_REASON_UNSPECIFIED"
    STALE = "FLAG_REASON_STALE"
    INCORRECT = "FLAG_REASON_INCORRECT"
    DUPLICATE = "FLAG_REASON_DUPLICATE"


class Flag(BaseModel):
    """A recorded flag against a knowledge unit."""

    reason: FlagReason
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="before")
    @classmethod
    def _normalize_legacy_reason(cls, data: dict) -> dict:
        """Map pre-proto flag reason values to proto-canonical form."""
        if isinstance(data, dict):
            reason = data.get("reason")
            if isinstance(reason, str) and reason in _LEGACY_FLAG_REASON_MAP:
                data["reason"] = _LEGACY_FLAG_REASON_MAP[reason]
        return data


class Insight(BaseModel):
    """Tripartite insight: summary, detail, and recommended action."""

    summary: str
    detail: str
    action: str


class Context(BaseModel):
    """Language, framework, and pattern context for a knowledge unit."""

    languages: list[str] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)
    pattern: str = ""


class Evidence(BaseModel):
    """Evidence and confidence metrics for a knowledge unit."""

    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    confirmations: int = 1
    first_observed: datetime | None = None
    last_confirmed: datetime | None = None

    @model_validator(mode="before")
    @classmethod
    def _set_default_timestamps(cls, data: dict) -> dict:
        """Ensure timestamp consistency on creation."""
        if isinstance(data, dict):
            first = data.get("first_observed")
            last = data.get("last_confirmed")
            if first is None and last is None:
                now = datetime.now(UTC)
                data["first_observed"] = now
                data["last_confirmed"] = now
            elif first is None:
                data["first_observed"] = last
            elif last is None:
                data["last_confirmed"] = first
        return data


class KnowledgeUnit(BaseModel):
    """A single unit of shared agent knowledge."""

    id: str
    version: int = 1
    domain: list[str] = Field(min_length=1)
    insight: Insight
    context: Context = Field(default_factory=Context)
    evidence: Evidence = Field(default_factory=Evidence)
    tier: Tier = Tier.LOCAL
    created_by: str = ""
    superseded_by: str | None = None
    flags: list[Flag] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _normalize_legacy_tier(cls, data: dict) -> dict:
        """Map pre-proto tier values to proto-canonical form."""
        if isinstance(data, dict):
            tier = data.get("tier")
            if isinstance(tier, str) and tier in _LEGACY_TIER_MAP:
                data["tier"] = _LEGACY_TIER_MAP[tier]
        return data


def _generate_ku_id() -> str:
    """Generate a prefixed UUID for knowledge unit identification."""
    return _KU_ID_PREFIX + uuid.uuid4().hex


def create_knowledge_unit(
    *,
    domain: list[str],
    insight: Insight,
    context: Context | None = None,
    tier: Tier = Tier.LOCAL,
    created_by: str = "",
) -> KnowledgeUnit:
    """Create a new knowledge unit with an auto-generated ID."""
    return KnowledgeUnit(
        id=_generate_ku_id(),
        domain=domain,
        insight=insight,
        context=context or Context(),
        tier=tier,
        created_by=created_by,
    )
