"""Tests for Client."""

from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

import httpx
import pytest

from cq.client import Client
from cq.models import FlagReason


@pytest.fixture()
def client(tmp_path: Path) -> Iterator[Client]:
    c = Client(local_db_path=tmp_path / "test.db")
    yield c
    c.close()


class TestLocalOnlyMode:
    def test_no_remote_addr_by_default(self, client: Client):
        assert client.addr is None

    def test_propose_and_query_roundtrip(self, client: Client):
        ku = client.propose(
            summary="Use connection pooling",
            detail="Connections are expensive.",
            action="Configure pool max size.",
            domains=["databases"],
        )
        assert ku.id.startswith("ku_")

        results = client.query(["databases"])
        assert len(results) == 1
        assert results[0].id == ku.id

    def test_confirm_boosts_confidence(self, client: Client):
        ku = client.propose(
            summary="Test insight",
            detail="Detail.",
            action="Action.",
            domains=["testing"],
        )
        confirmed = client.confirm(ku.id)
        assert confirmed.evidence.confidence == pytest.approx(0.6)
        assert confirmed.evidence.confirmations == 2

    def test_flag_reduces_confidence(self, client: Client):
        ku = client.propose(
            summary="Test insight",
            detail="Detail.",
            action="Action.",
            domains=["testing"],
        )
        flagged = client.flag(ku.id, FlagReason.STALE)
        assert flagged.evidence.confidence == pytest.approx(0.35)
        assert len(flagged.flags) == 1
        assert flagged.flags[0].reason == FlagReason.STALE

    def test_confirm_missing_unit_raises(self, client: Client):
        with pytest.raises(KeyError, match="ku_nonexistent"):
            client.confirm("ku_nonexistent")

    def test_flag_missing_unit_raises(self, client: Client):
        with pytest.raises(KeyError, match="ku_nonexistent"):
            client.flag("ku_nonexistent", FlagReason.STALE)

    def test_status_returns_store_stats(self, client: Client):
        client.propose(
            summary="Test",
            detail="Detail.",
            action="Action.",
            domains=["api"],
        )
        stats = client.status()
        assert stats.total_count == 1
        assert "api" in stats.domain_counts

    def test_drain_raises_without_remote(self, client: Client):
        with pytest.raises(RuntimeError, match="No remote API configured"):
            client.drain()

    def test_context_manager(self, tmp_path: Path):
        with Client(local_db_path=tmp_path / "test.db") as c:
            ku = c.propose(
                summary="Test",
                detail="Detail.",
                action="Action.",
                domains=["testing"],
            )
            assert c.query(["testing"])[0].id == ku.id

    def test_propose_with_language_and_framework(self, client: Client):
        ku = client.propose(
            summary="Use Django ORM",
            detail="Better than raw SQL.",
            action="Use QuerySet API.",
            domains=["databases"],
            language="python",
            framework="django",
        )
        assert ku.context.languages == ["python"]
        assert ku.context.frameworks == ["django"]

    def test_query_language_boosts_ranking(self, client: Client):
        client.propose(
            summary="Python insight",
            detail="Detail.",
            action="Action.",
            domains=["api"],
            language="python",
        )
        client.propose(
            summary="Go insight",
            detail="Detail.",
            action="Action.",
            domains=["api"],
            language="go",
        )
        results = client.query(["api"], language="python")
        assert len(results) == 2
        assert results[0].context.languages == ["python"]


class TestFullLifecycle:
    def test_propose_confirm_query_flag(self, client: Client):
        ku = client.propose(
            summary="Stripe 402 means card_declined",
            detail="Check error.code, not error.type.",
            action="Handle card_declined explicitly.",
            domains=["api", "stripe"],
            language="python",
        )

        results = client.query(["api", "stripe"], language="python")
        assert len(results) == 1
        assert results[0].evidence.confidence == 0.5

        client.confirm(ku.id)
        results = client.query(["api", "stripe"])
        assert results[0].evidence.confidence == pytest.approx(0.6)

        client.flag(ku.id, FlagReason.STALE)
        results = client.query(["api", "stripe"])
        assert results[0].evidence.confidence == pytest.approx(0.45)
        assert len(results[0].flags) == 1


class TestRemoteConfig:
    def test_reads_addr_from_env(self, tmp_path: Path):
        with patch.dict("os.environ", {"CQ_ADDR": "http://localhost:8742"}):
            c = Client(local_db_path=tmp_path / "test.db")
            assert c.addr == "http://localhost:8742"
            c.close()

    def test_constructor_addr_takes_precedence(self, tmp_path: Path):
        with patch.dict("os.environ", {"CQ_ADDR": "http://env-addr"}):
            c = Client(
                addr="http://explicit-addr",
                local_db_path=tmp_path / "test.db",
            )
            assert c.addr == "http://explicit-addr"
            c.close()

    def test_reads_db_path_from_env(self, tmp_path: Path):
        db = tmp_path / "custom.db"
        with patch.dict("os.environ", {"CQ_LOCAL_DB_PATH": str(db)}):
            c = Client()
            assert c._store.db_path == db
            c.close()


class TestRemoteIntegration:
    def test_remote_query_merges_with_local(self, tmp_path: Path, httpx_mock):
        """Remote results are merged with local results."""
        remote_unit = {
            "id": "ku_remote123",
            "domain": ["api"],
            "insight": {"summary": "S", "detail": "D", "action": "A"},
            "evidence": {
                "confidence": 0.8,
                "confirmations": 5,
                "first_observed": "2025-01-01T00:00:00Z",
                "last_confirmed": "2025-01-01T00:00:00Z",
            },
            "tier": "TIER_PRIVATE",
        }
        httpx_mock.add_response(json={}, status_code=200)  # Accept /propose.
        httpx_mock.add_response(
            url=httpx.URL("http://test-remote/query", params={"domain": ["api"], "limit": "5"}),
            json=[remote_unit],
        )

        c = Client(
            addr="http://test-remote",
            local_db_path=tmp_path / "test.db",
        )
        c.propose(
            summary="Local insight",
            detail="D",
            action="A",
            domains=["api"],
        )

        results = c.query(["api"])
        assert len(results) == 2
        ids = {r.id for r in results}
        assert "ku_remote123" in ids
        c.close()

    def test_remote_failure_falls_back_to_local(self, tmp_path: Path, httpx_mock):
        """When remote API is unreachable, local results still returned."""
        httpx_mock.add_exception(httpx.ConnectError("Connection refused"))

        c = Client(
            addr="http://unreachable",
            local_db_path=tmp_path / "test.db",
        )
        c.propose(
            summary="Local only",
            detail="D",
            action="A",
            domains=["api"],
        )

        results = c.query(["api"])
        assert len(results) == 1
        c.close()


@pytest.fixture()
def httpx_mock():
    """Minimal httpx mock for testing remote API calls."""
    responses: list[dict] = []
    exceptions: list[Exception] = []

    class _Mock:
        def add_response(self, url=None, json=None, status_code=200):
            responses.append({"url": url, "json": json, "status_code": status_code})

        def add_exception(self, exc: Exception):
            exceptions.append(exc)

    mock = _Mock()

    def patched_send(self, request, **kwargs):
        if exceptions:
            raise exceptions.pop(0)
        for idx, resp_config in enumerate(responses):
            expected_url = resp_config["url"]
            if expected_url is None or request.url == expected_url:
                responses.pop(idx)
                return httpx.Response(
                    status_code=resp_config["status_code"],
                    json=resp_config["json"],
                    request=request,
                )
        return httpx.Response(status_code=404, request=request)

    with patch.object(httpx.Client, "send", patched_send):
        yield mock
