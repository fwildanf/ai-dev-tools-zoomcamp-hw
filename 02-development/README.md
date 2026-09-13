# Premier League Scoreboard

App name: `pl_scoreboard`.

Shows the current Premier League table and this week's results and fixtures. The frontend still uses a local mock; the FastAPI backend serves the same snapshot from an in-memory store.

## Frontend (mocked)

Open [frontent/](frontent/) — a static page that loads the table and this week's matches through `frontent/js/api.js`.

```bash
cd frontent
python3 -m http.server 8000
```

Open <http://127.0.0.1:8000/>. A local server is required because the page uses ES modules.

## Backend

Contract: [openapi.yaml](openapi.yaml). Data comes from [backend/db.py](backend/db.py) (mock database).

### Setup and run

From this directory (`02-development/`, not `backend/`):

```bash
uv sync --group dev && uv run uvicorn backend.main:app --reload --port 8000
```

- Health: <http://127.0.0.1:8000/health>
- Scoreboard: <http://127.0.0.1:8000/api/scoreboard>
- Docs: <http://127.0.0.1:8000/docs>

### Tests

```bash
uv run pytest
```

Tests use the mock database and do not call football-data.org.

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
- In-memory mock database (replace later)

## Project Documentation

- [Product specs](_docs/specs.md)
- [Agent notes](AGENTS.md)
- [OpenAPI](openapi.yaml)

## MVP Boundaries

No auto-refresh, in-play events, past seasons, club pages, extra stats, accounts, or manual result entry.
