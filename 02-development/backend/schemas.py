from typing import Literal

from pydantic import BaseModel, ConfigDict


class Health(BaseModel):
    status: Literal["ok"]


class Standing(BaseModel):
    model_config = ConfigDict(extra="forbid")

    position: int
    club: str
    played: int
    won: int
    drawn: int
    lost: int
    goalsFor: int
    goalsAgainst: int
    goalDifference: int
    points: int


class Match(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    utcKickoff: str
    status: Literal["FINISHED", "SCHEDULED"]
    home: str
    away: str
    homeScore: int | None
    awayScore: int | None


class Scoreboard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    season: str
    matchweek: int
    competition: str
    standings: list[Standing]
    matches: list[Match]


class Error(BaseModel):
    detail: str
