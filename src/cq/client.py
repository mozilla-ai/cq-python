"""Client — the public interface to the cq knowledge commons.

Handles remote mode (HTTP calls to a cq API) and local mode
(SQLite at $XDG_DATA_HOME/cq/local.db), with fallback between them.
"""

import logging
import os
from pathlib import Path

import httpx
from pydantic import ValidationError

from .models import (
    Context,
    FlagReason,
    Insight,
    KnowledgeUnit,
    Tier,
    create_knowledge_unit,
)
from .scoring import apply_confirmation, apply_flag
from .store import LocalStore, StoreStats

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 5.0


class RemoteError(Exception):
    """Raised when the remote API explicitly rejects a request."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Remote API rejected request ({status_code}): {detail}")


class Client:
    """Client for the cq shared knowledge commons.

    Queries, proposes, confirms, and flags knowledge units against a
    remote cq API or a local SQLite store.

    When no remote address is configured, operates in local-only mode.
    When the remote API is unreachable, falls back to local storage.
    """

    def __init__(
        self,
        addr: str | None = None,
        local_db_path: Path | None = None,
    ) -> None:
        """Initialize the client.

        Args:
            addr: Remote cq API address. Reads from CQ_ADDR
                env var if not provided. None = local-only mode.
            local_db_path: Local SQLite path. Reads from CQ_LOCAL_DB_PATH
                env var if not provided. Defaults to $XDG_DATA_HOME/cq/local.db.
        """
        self._addr = addr or os.environ.get("CQ_ADDR")
        db_path = local_db_path or _db_path_from_env()
        self._store = LocalStore(db_path=db_path)
        self._http: httpx.Client | None = None
        if self._addr:
            api_key = os.environ.get("CQ_API_KEY", "")
            headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            self._http = httpx.Client(
                base_url=self._addr,
                timeout=_DEFAULT_TIMEOUT,
                headers=headers,
            )

    def close(self) -> None:
        """Close the local store and HTTP client."""
        self._store.close()
        if self._http is not None:
            self._http.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    @property
    def addr(self) -> str | None:
        """The configured remote API address, or None for local-only mode."""
        return self._addr

    def query(
        self,
        domains: list[str],
        *,
        language: str | None = None,
        framework: str | None = None,
        limit: int = 5,
    ) -> list[KnowledgeUnit]:
        """Search for knowledge units by domain tags.

        Queries both the local store and remote API (if configured),
        merging and deduplicating results.
        """
        local_results = self._store.query(domains, language=language, framework=framework, limit=limit)

        if self._http is None:
            return local_results

        remote_results = self._remote_query(domains, language=language, framework=framework, limit=limit)
        return _merge_results(local_results, remote_results, limit)

    def propose(
        self,
        summary: str,
        detail: str,
        action: str,
        domains: list[str],
        *,
        language: str | None = None,
        framework: str | None = None,
        pattern: str = "",
        created_by: str = "",
    ) -> KnowledgeUnit:
        """Propose a new knowledge unit.

        When a remote API is configured, sends to remote only. Falls back
        to local storage when the remote is unreachable. Raises RemoteError
        if the remote explicitly rejects the unit.
        """
        context = Context(
            languages=[language] if language else [],
            frameworks=[framework] if framework else [],
            pattern=pattern,
        )
        unit = create_knowledge_unit(
            domain=domains,
            insight=Insight(summary=summary, detail=detail, action=action),
            context=context,
            created_by=created_by,
        )
        if self._http is not None:
            if self._remote_propose(unit):
                return unit
            # Remote unreachable — fall back to local storage.
            logger.info("Remote unreachable; storing unit %s locally as fallback.", unit.id)

        self._store.insert(unit)
        return unit

    def confirm(self, unit_id: str) -> KnowledgeUnit:
        """Confirm a knowledge unit, boosting its confidence.

        Raises:
            KeyError: If the unit is not found locally.
        """
        unit = self._store.get(unit_id)
        if unit is None:
            raise KeyError(f"Knowledge unit not found: {unit_id}")

        confirmed = apply_confirmation(unit)
        self._store.update(confirmed)

        if self._http is not None:
            self._remote_confirm(unit_id)

        return confirmed

    def flag(self, unit_id: str, reason: FlagReason) -> KnowledgeUnit:
        """Flag a knowledge unit, reducing its confidence.

        Raises:
            KeyError: If the unit is not found locally.
        """
        unit = self._store.get(unit_id)
        if unit is None:
            raise KeyError(f"Knowledge unit not found: {unit_id}")

        flagged = apply_flag(unit, reason)
        self._store.update(flagged)

        if self._http is not None:
            self._remote_flag(unit_id, reason)

        return flagged

    def status(self) -> StoreStats:
        """Return local store statistics."""
        return self._store.stats()

    @staticmethod
    def prompt() -> str:
        """Return the canonical cq agent protocol prompt."""
        from .protocol import prompt as _prompt

        return _prompt()

    def drain(self) -> int:
        """Push all local-only units to the remote API.

        Returns:
            The number of units successfully pushed.

        Raises:
            RuntimeError: If no remote API is configured.
        """
        if self._http is None:
            raise RuntimeError("No remote API configured")

        units = self._store.all()
        pushed = 0
        for unit in units:
            if unit.tier == Tier.LOCAL:
                try:
                    if self._remote_propose(unit):
                        self._store.delete(unit.id)
                        pushed += 1
                except (httpx.HTTPError, RemoteError):
                    logger.warning("Failed to drain unit %s", unit.id, exc_info=True)
        return pushed

    # -- Remote HTTP helpers (graceful degradation) --

    def _remote_query(
        self,
        domains: list[str],
        *,
        language: str | None = None,
        framework: str | None = None,
        limit: int = 5,
    ) -> list[KnowledgeUnit]:
        """Query the remote API, returning empty list on failure."""
        assert self._http is not None
        params: dict[str, str | int | list[str]] = {
            "domain": domains,
            "limit": limit,
        }
        if language:
            params["language"] = language
        if framework:
            params["framework"] = framework
        try:
            resp = self._http.get("/query", params=params)
            resp.raise_for_status()
            return [KnowledgeUnit.model_validate(item) for item in resp.json()]
        except (httpx.HTTPError, ValueError, ValidationError):
            logger.warning("Remote query failed", exc_info=True)
            return []

    def _remote_propose(self, unit: KnowledgeUnit) -> bool:
        """Push a unit to the remote API.

        Returns:
            True if the remote accepted the unit, False on transport error.

        Raises:
            RemoteError: If the remote API explicitly rejects the request.
        """
        assert self._http is not None
        body = {
            "domain": unit.domain,
            "insight": unit.insight.model_dump(mode="json"),
            "context": unit.context.model_dump(mode="json"),
            "created_by": unit.created_by,
        }
        try:
            resp = self._http.post("/propose", json=body)
            resp.raise_for_status()
            return True
        except httpx.HTTPStatusError as exc:
            raise RemoteError(
                status_code=exc.response.status_code,
                detail=exc.response.text,
            ) from exc
        except httpx.HTTPError:
            logger.debug("Remote propose unreachable", exc_info=True)
            return False

    def _remote_confirm(self, unit_id: str) -> None:
        """Confirm a unit on the remote API."""
        assert self._http is not None
        try:
            resp = self._http.post(f"/confirm/{unit_id}")
            resp.raise_for_status()
        except httpx.HTTPError:
            logger.debug("Remote confirm failed", exc_info=True)

    def _remote_flag(self, unit_id: str, reason: FlagReason) -> None:
        """Flag a unit on the remote API."""
        assert self._http is not None
        try:
            resp = self._http.post(
                f"/flag/{unit_id}",
                json={"reason": reason.value},
            )
            resp.raise_for_status()
        except httpx.HTTPError:
            logger.debug("Remote flag failed", exc_info=True)


def _db_path_from_env() -> Path | None:
    """Read local DB path from environment, or return None for default."""
    env_path = os.environ.get("CQ_LOCAL_DB_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return None


def _merge_results(
    local: list[KnowledgeUnit],
    remote: list[KnowledgeUnit],
    limit: int,
) -> list[KnowledgeUnit]:
    """Merge and deduplicate results, preferring local copies."""
    seen: set[str] = set()
    merged: list[KnowledgeUnit] = []
    for unit in [*local, *remote]:
        if unit.id not in seen:
            seen.add(unit.id)
            merged.append(unit)
    return merged[:limit]
