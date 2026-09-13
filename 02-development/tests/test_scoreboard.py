import pytest
from fastapi.testclient import TestClient

from backend.database import get_session_factory, init_db, reset_engine
from backend.main import app
from backend.repository import add_match


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")
    monkeypatch.delenv("SCOREBOARD_SEED", raising=False)
    reset_engine()
    with TestClient(app) as test_client:
        yield test_client
    reset_engine()


@pytest.fixture
def empty_client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'empty.db'}")
    monkeypatch.setenv("SCOREBOARD_SEED", "0")
    reset_engine()
    with TestClient(app) as test_client:
        yield test_client
    reset_engine()


STANDING_KEYS = {
    "position",
    "club",
    "played",
    "won",
    "drawn",
    "lost",
    "goalsFor",
    "goalsAgainst",
    "goalDifference",
    "points",
}
MATCH_KEYS = {
    "id",
    "utcKickoff",
    "status",
    "home",
    "away",
    "homeScore",
    "awayScore",
}


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_scoreboard_returns_current_table_and_this_week(client):
    response = client.get("/api/scoreboard")
    assert response.status_code == 200
    body = response.json()
    assert body["competition"] == "Premier League"
    assert body["season"]
    assert isinstance(body["matchweek"], int) and body["matchweek"] >= 1
    assert len(body["standings"]) == 20
    assert len(body["matches"]) >= 1


def test_standings_have_required_fields_and_are_ordered(client):
    body = client.get("/api/scoreboard").json()
    positions = [row["position"] for row in body["standings"]]
    assert positions == list(range(1, 21))
    for row in body["standings"]:
        assert set(row) == STANDING_KEYS
        assert row["played"] == row["won"] + row["drawn"] + row["lost"]
        assert row["goalDifference"] == row["goalsFor"] - row["goalsAgainst"]
        assert row["points"] == row["won"] * 3 + row["drawn"]


def test_finished_matches_have_scores_and_scheduled_do_not(client):
    body = client.get("/api/scoreboard").json()
    statuses = {match["status"] for match in body["matches"]}
    assert statuses <= {"FINISHED", "SCHEDULED"}
    assert "FINISHED" in statuses
    assert "SCHEDULED" in statuses
    for match in body["matches"]:
        assert set(match) == MATCH_KEYS
        if match["status"] == "FINISHED":
            assert match["homeScore"] is not None
            assert match["awayScore"] is not None
        else:
            assert match["homeScore"] is None
            assert match["awayScore"] is None


def test_get_match_by_id(client):
    scoreboard = client.get("/api/scoreboard").json()
    match_id = scoreboard["matches"][0]["id"]
    response = client.get(f"/api/matches/{match_id}")
    assert response.status_code == 200
    assert response.json()["id"] == match_id
    assert set(response.json()) == MATCH_KEYS


def test_get_match_unknown_id_returns_404(client):
    response = client.get("/api/matches/does-not-exist")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_frontend_index_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "pl_scoreboard" in response.text


def test_empty_database_returns_empty_lists(empty_client):
    body = empty_client.get("/api/scoreboard").json()
    assert body["standings"] == []
    assert body["matches"] == []


def test_seed_is_idempotent(client):
    init_db()
    init_db()
    body = client.get("/api/scoreboard").json()
    assert len(body["standings"]) == 20
    assert len(body["matches"]) == 10


def test_added_match_is_visible_on_later_request(client):
    session = get_session_factory()()
    try:
        add_match(
            session,
            {
                "id": "mw4-extra",
                "utcKickoff": "2026-09-15T12:00:00Z",
                "status": "SCHEDULED",
                "home": "Liverpool",
                "away": "Arsenal",
                "homeScore": None,
                "awayScore": None,
            },
        )
        session.commit()
    finally:
        session.close()

    response = client.get("/api/matches/mw4-extra")
    assert response.status_code == 200
    assert response.json()["home"] == "Liverpool"
    assert response.json()["status"] == "SCHEDULED"
    board = client.get("/api/scoreboard").json()
    assert any(match["id"] == "mw4-extra" for match in board["matches"])
