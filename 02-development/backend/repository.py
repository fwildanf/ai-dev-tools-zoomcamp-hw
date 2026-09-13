from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models import MatchRow, ScoreboardMeta, StandingRow
from backend.seed import SNAPSHOT


def _standing_to_dict(row: StandingRow) -> dict:
    return {
        "position": row.position,
        "club": row.club,
        "played": row.played,
        "won": row.won,
        "drawn": row.drawn,
        "lost": row.lost,
        "goalsFor": row.goals_for,
        "goalsAgainst": row.goals_against,
        "goalDifference": row.goal_difference,
        "points": row.points,
    }


def _match_to_dict(row: MatchRow) -> dict:
    return {
        "id": row.id,
        "utcKickoff": row.utc_kickoff,
        "status": row.status,
        "home": row.home,
        "away": row.away,
        "homeScore": row.home_score,
        "awayScore": row.away_score,
    }


def get_scoreboard(session: Session) -> dict:
    meta = session.scalar(select(ScoreboardMeta).order_by(ScoreboardMeta.id).limit(1))
    standings = session.scalars(select(StandingRow).order_by(StandingRow.position)).all()
    matches = session.scalars(select(MatchRow).order_by(MatchRow.utc_kickoff, MatchRow.id)).all()
    if meta is None:
        return {
            "season": "",
            "matchweek": 1,
            "competition": "Premier League",
            "standings": [],
            "matches": [],
        }
    return {
        "season": meta.season,
        "matchweek": meta.matchweek,
        "competition": meta.competition,
        "standings": [_standing_to_dict(row) for row in standings],
        "matches": [_match_to_dict(row) for row in matches],
    }


def get_match(session: Session, match_id: str) -> dict | None:
    row = session.get(MatchRow, match_id)
    if row is None:
        return None
    return _match_to_dict(row)


def add_match(session: Session, match: dict) -> dict:
    row = MatchRow(
        id=match["id"],
        utc_kickoff=match["utcKickoff"],
        status=match["status"],
        home=match["home"],
        away=match["away"],
        home_score=match.get("homeScore"),
        away_score=match.get("awayScore"),
    )
    session.add(row)
    session.flush()
    return _match_to_dict(row)


def seed_if_empty(session: Session) -> bool:
    count = session.scalar(select(func.count()).select_from(ScoreboardMeta)) or 0
    if count:
        return False
    session.add(
        ScoreboardMeta(
            season=SNAPSHOT["season"],
            matchweek=SNAPSHOT["matchweek"],
            competition=SNAPSHOT["competition"],
        )
    )
    for row in SNAPSHOT["standings"]:
        session.add(
            StandingRow(
                position=row["position"],
                club=row["club"],
                played=row["played"],
                won=row["won"],
                drawn=row["drawn"],
                lost=row["lost"],
                goals_for=row["goalsFor"],
                goals_against=row["goalsAgainst"],
                goal_difference=row["goalDifference"],
                points=row["points"],
            )
        )
    for row in SNAPSHOT["matches"]:
        session.add(
            MatchRow(
                id=row["id"],
                utc_kickoff=row["utcKickoff"],
                status=row["status"],
                home=row["home"],
                away=row["away"],
                home_score=row["homeScore"],
                away_score=row["awayScore"],
            )
        )
    return True
