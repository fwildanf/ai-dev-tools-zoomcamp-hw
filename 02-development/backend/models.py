from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ScoreboardMeta(Base):
    __tablename__ = "scoreboard_meta"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season: Mapped[str] = mapped_column(String(16), nullable=False)
    matchweek: Mapped[int] = mapped_column(Integer, nullable=False)
    competition: Mapped[str] = mapped_column(String(64), nullable=False)


class StandingRow(Base):
    __tablename__ = "standings"

    position: Mapped[int] = mapped_column(Integer, primary_key=True)
    club: Mapped[str] = mapped_column(String(128), nullable=False)
    played: Mapped[int] = mapped_column(Integer, nullable=False)
    won: Mapped[int] = mapped_column(Integer, nullable=False)
    drawn: Mapped[int] = mapped_column(Integer, nullable=False)
    lost: Mapped[int] = mapped_column(Integer, nullable=False)
    goals_for: Mapped[int] = mapped_column(Integer, nullable=False)
    goals_against: Mapped[int] = mapped_column(Integer, nullable=False)
    goal_difference: Mapped[int] = mapped_column(Integer, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)


class MatchRow(Base):
    __tablename__ = "matches"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    utc_kickoff: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    home: Mapped[str] = mapped_column(String(128), nullable=False)
    away: Mapped[str] = mapped_column(String(128), nullable=False)
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
