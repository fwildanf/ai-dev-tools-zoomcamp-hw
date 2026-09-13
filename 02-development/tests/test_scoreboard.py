from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

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


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_scoreboard_returns_current_table_and_this_week():
    response = client.get("/api/scoreboard")
    assert response.status_code == 200
    body = response.json()
    assert body["competition"] == "Premier League"
    assert body["season"]
    assert isinstance(body["matchweek"], int) and body["matchweek"] >= 1
    assert len(body["standings"]) == 20
    assert len(body["matches"]) >= 1


def test_standings_have_required_fields_and_are_ordered():
    body = client.get("/api/scoreboard").json()
    positions = [row["position"] for row in body["standings"]]
    assert positions == list(range(1, 21))
    for row in body["standings"]:
        assert set(row) == STANDING_KEYS
        assert row["played"] == row["won"] + row["drawn"] + row["lost"]
        assert row["goalDifference"] == row["goalsFor"] - row["goalsAgainst"]
        assert row["points"] == row["won"] * 3 + row["drawn"]


def test_finished_matches_have_scores_and_scheduled_do_not():
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


def test_get_match_by_id():
    scoreboard = client.get("/api/scoreboard").json()
    match_id = scoreboard["matches"][0]["id"]
    response = client.get(f"/api/matches/{match_id}")
    assert response.status_code == 200
    assert response.json()["id"] == match_id
    assert set(response.json()) == MATCH_KEYS


def test_get_match_unknown_id_returns_404():
    response = client.get("/api/matches/does-not-exist")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_frontend_index_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "pl_scoreboard" in response.text
