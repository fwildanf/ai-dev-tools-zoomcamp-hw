# Premier League Scoreboard

Django project: `pl_scoreboard`.

Local Django web app that shows the current Premier League table and this week's results and fixtures. Data comes from football-data.org on page load and is cached in SQLite.

This folder currently has specs only. The app is not implemented yet.

## Features (planned)

- Current-season league table (rank, club, played, W/D/L, GF/GA, GD, points)
- This week's finished matches with scores
- This week's upcoming matches with kickoff times
- Fetch on page load with a short local cache
- No login

## Technology (planned)

- Python 3.14+
- Django 5.2
- SQLite cache
- `uv` for dependency management
- [football-data.org](https://www.football-data.org/) (`PL` competition)

## Setup

From this directory, after the Django app exists:

```bash
uv sync
uv run python manage.py migrate
```

Copy `.env.example` to `.env` and set `FOOTBALL_DATA_API_TOKEN`.

## Run the Development Server

```bash
uv run python manage.py runserver
```

## Run Tests

```bash
uv run python manage.py test
```

Tests must mock the football API and must not call the live service.

## Project Documentation

- [Product specs](_docs/specs.md)
- [Agent notes](AGENTS.md)

## MVP Boundaries

No auto-refresh, in-play events, past seasons, club pages, extra stats, accounts, or manual result entry.
