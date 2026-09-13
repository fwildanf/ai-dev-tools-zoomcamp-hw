# Agent notes — Premier League Scoreboard

Follow [_docs/specs.md](_docs/specs.md). Do not expand the MVP unless the user asks.

## Stack

- FastAPI backend in `backend/`, project name `pl_scoreboard`
- Python 3.14+, `uv`, SQLAlchemy (database-agnostic; default SQLite)
- Set `DATABASE_URL` to switch engines (e.g. PostgreSQL later)
- Contract: [openapi.yaml](openapi.yaml)
- Work only inside `02-development/`
- Frontend lives in `frontent/`; all backend access goes through `frontent/js/api.js` (`GET /api/scoreboard` and `GET /api/matches/{id}`)
- FastAPI serves the UI from `/` so frontend and API share origin

## Product

- One public page: current PL table **and** this week's results/fixtures
- Current season only
- Fetch on page load; short SQLite TTL cache
- No auto-refresh, websockets, or in-play events
- No accounts, club pages, form column, top scorers, or xG

## API

- Contract: [openapi.yaml](openapi.yaml)
- SQLAlchemy repository in `backend/repository.py`; engine from `DATABASE_URL`
- Tests use an isolated SQLite file and must not call football-data.org
- Later: football-data.org (`PL`), token in `.env` as `FOOTBALL_DATA_API_TOKEN`

## Docs

- Humans: [README.md](README.md)
- Scope: [_docs/specs.md](_docs/specs.md)
- API: [openapi.yaml](openapi.yaml)
