"""In-memory scoreboard store. Replace with a real database later."""

from copy import deepcopy

_SCOREBOARD = {
    "season": "2026/27",
    "matchweek": 4,
    "competition": "Premier League",
    "standings": [
        {"position": 1, "club": "Liverpool", "played": 4, "won": 4, "drawn": 0, "lost": 0, "goalsFor": 10, "goalsAgainst": 2, "goalDifference": 8, "points": 12},
        {"position": 2, "club": "Arsenal", "played": 4, "won": 3, "drawn": 1, "lost": 0, "goalsFor": 9, "goalsAgainst": 2, "goalDifference": 7, "points": 10},
        {"position": 3, "club": "Manchester City", "played": 4, "won": 3, "drawn": 1, "lost": 0, "goalsFor": 11, "goalsAgainst": 4, "goalDifference": 7, "points": 10},
        {"position": 4, "club": "Chelsea", "played": 4, "won": 3, "drawn": 0, "lost": 1, "goalsFor": 8, "goalsAgainst": 4, "goalDifference": 4, "points": 9},
        {"position": 5, "club": "Tottenham Hotspur", "played": 4, "won": 2, "drawn": 2, "lost": 0, "goalsFor": 7, "goalsAgainst": 3, "goalDifference": 4, "points": 8},
        {"position": 6, "club": "Aston Villa", "played": 4, "won": 2, "drawn": 1, "lost": 1, "goalsFor": 6, "goalsAgainst": 4, "goalDifference": 2, "points": 7},
        {"position": 7, "club": "Newcastle United", "played": 4, "won": 2, "drawn": 1, "lost": 1, "goalsFor": 6, "goalsAgainst": 5, "goalDifference": 1, "points": 7},
        {"position": 8, "club": "Brighton & Hove Albion", "played": 4, "won": 2, "drawn": 1, "lost": 1, "goalsFor": 5, "goalsAgainst": 4, "goalDifference": 1, "points": 7},
        {"position": 9, "club": "Bournemouth", "played": 4, "won": 2, "drawn": 0, "lost": 2, "goalsFor": 6, "goalsAgainst": 6, "goalDifference": 0, "points": 6},
        {"position": 10, "club": "Fulham", "played": 4, "won": 1, "drawn": 3, "lost": 0, "goalsFor": 5, "goalsAgainst": 4, "goalDifference": 1, "points": 6},
        {"position": 11, "club": "Crystal Palace", "played": 4, "won": 1, "drawn": 2, "lost": 1, "goalsFor": 4, "goalsAgainst": 4, "goalDifference": 0, "points": 5},
        {"position": 12, "club": "Everton", "played": 4, "won": 1, "drawn": 2, "lost": 1, "goalsFor": 4, "goalsAgainst": 5, "goalDifference": -1, "points": 5},
        {"position": 13, "club": "Manchester United", "played": 4, "won": 1, "drawn": 1, "lost": 2, "goalsFor": 5, "goalsAgainst": 7, "goalDifference": -2, "points": 4},
        {"position": 14, "club": "Brentford", "played": 4, "won": 1, "drawn": 1, "lost": 2, "goalsFor": 5, "goalsAgainst": 7, "goalDifference": -2, "points": 4},
        {"position": 15, "club": "West Ham United", "played": 4, "won": 1, "drawn": 1, "lost": 2, "goalsFor": 4, "goalsAgainst": 7, "goalDifference": -3, "points": 4},
        {"position": 16, "club": "Nottingham Forest", "played": 4, "won": 1, "drawn": 0, "lost": 3, "goalsFor": 4, "goalsAgainst": 8, "goalDifference": -4, "points": 3},
        {"position": 17, "club": "Wolverhampton Wanderers", "played": 4, "won": 0, "drawn": 2, "lost": 2, "goalsFor": 3, "goalsAgainst": 7, "goalDifference": -4, "points": 2},
        {"position": 18, "club": "Leeds United", "played": 4, "won": 0, "drawn": 2, "lost": 2, "goalsFor": 3, "goalsAgainst": 8, "goalDifference": -5, "points": 2},
        {"position": 19, "club": "Burnley", "played": 4, "won": 0, "drawn": 1, "lost": 3, "goalsFor": 2, "goalsAgainst": 8, "goalDifference": -6, "points": 1},
        {"position": 20, "club": "Sunderland", "played": 4, "won": 0, "drawn": 0, "lost": 4, "goalsFor": 2, "goalsAgainst": 11, "goalDifference": -9, "points": 0},
    ],
    "matches": [
        {"id": "mw4-1", "utcKickoff": "2026-09-12T11:30:00Z", "status": "FINISHED", "home": "Liverpool", "away": "Burnley", "homeScore": 3, "awayScore": 0},
        {"id": "mw4-2", "utcKickoff": "2026-09-12T14:00:00Z", "status": "FINISHED", "home": "Arsenal", "away": "Nottingham Forest", "homeScore": 2, "awayScore": 0},
        {"id": "mw4-3", "utcKickoff": "2026-09-12T14:00:00Z", "status": "FINISHED", "home": "Bournemouth", "away": "Brighton & Hove Albion", "homeScore": 1, "awayScore": 2},
        {"id": "mw4-4", "utcKickoff": "2026-09-12T16:30:00Z", "status": "FINISHED", "home": "Chelsea", "away": "Brentford", "homeScore": 2, "awayScore": 1},
        {"id": "mw4-5", "utcKickoff": "2026-09-13T13:00:00Z", "status": "FINISHED", "home": "Everton", "away": "Aston Villa", "homeScore": 1, "awayScore": 1},
        {"id": "mw4-6", "utcKickoff": "2026-09-13T15:30:00Z", "status": "SCHEDULED", "home": "Manchester City", "away": "Manchester United", "homeScore": None, "awayScore": None},
        {"id": "mw4-7", "utcKickoff": "2026-09-13T18:00:00Z", "status": "SCHEDULED", "home": "Newcastle United", "away": "Tottenham Hotspur", "homeScore": None, "awayScore": None},
        {"id": "mw4-8", "utcKickoff": "2026-09-14T13:00:00Z", "status": "SCHEDULED", "home": "Fulham", "away": "Leeds United", "homeScore": None, "awayScore": None},
        {"id": "mw4-9", "utcKickoff": "2026-09-14T15:30:00Z", "status": "SCHEDULED", "home": "West Ham United", "away": "Crystal Palace", "homeScore": None, "awayScore": None},
        {"id": "mw4-10", "utcKickoff": "2026-09-14T18:00:00Z", "status": "SCHEDULED", "home": "Wolverhampton Wanderers", "away": "Sunderland", "homeScore": None, "awayScore": None},
    ],
}


def get_scoreboard() -> dict:
    return deepcopy(_SCOREBOARD)


def get_match(match_id: str) -> dict | None:
    for match in _SCOREBOARD["matches"]:
        if match["id"] == match_id:
            return deepcopy(match)
    return None
