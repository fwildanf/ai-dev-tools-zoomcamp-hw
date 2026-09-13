# Premier League Scoreboard

App name: `pl_scoreboard`.

Shows the current Premier League table and this week's results and fixtures. The FastAPI app serves the UI and the API from the same origin.

## Run

From this directory (`02-development/`, not `backend/`):

```bash
uv sync --group dev && uv run uvicorn backend.main:app --reload --port 8000
```

Then open <http://127.0.0.1:8000/>.

- Scoreboard UI: <http://127.0.0.1:8000/>
- API: <http://127.0.0.1:8000/api/scoreboard>
- Docs: <http://127.0.0.1:8000/docs>

The page loads standings and matches with `GET /api/scoreboard`. Match details use `GET /api/matches/{id}`.

If you serve the static files on another port, `frontent/js/api.js` falls back to `http://127.0.0.1:8000`.

Contract: [openapi.yaml](openapi.yaml). Data is stored with SQLAlchemy (`backend/repository.py`). Default database is SQLite (`pl_scoreboard.db`); set `DATABASE_URL` to use another engine.

## Tests

```bash
uv run pytest
```

Tests use an isolated SQLite database and do not call football-data.org.

## Features

- Current-season league table (rank, club, played, W/D/L, GF/GA, GD, points)
- This week's finished matches with scores
- This week's upcoming matches with kickoff times
- Fetch on page load with a short local cache (frontend)
- No login

## Technology

- Python 3.14+
- FastAPI
- `uv`
- SQLAlchemy (SQLite by default; any SQLAlchemy URL via `DATABASE_URL`)

## Project Documentation

- [Product specs](_docs/specs.md)
- [Agent notes](AGENTS.md)
- [OpenAPI](openapi.yaml)

## MVP Boundaries

No auto-refresh, in-play events, past seasons, club pages, extra stats, accounts, or manual result entry.
