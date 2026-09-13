# Agent notes — Premier League Scoreboard

Follow [_docs/specs.md](_docs/specs.md). Do not expand the MVP unless the user asks.

## Stack

- Django web app, same shape as `01-ai-native-workflow`
- Python 3.14+, Django 5.2, `uv`, SQLite
- Work only inside `02-development/`

## Product

- One public page: current PL table **and** this week's results/fixtures
- Current season only
- Fetch on page load; short SQLite TTL cache
- No auto-refresh, websockets, or in-play events
- No accounts, club pages, form column, top scorers, or xG

## API

- football-data.org, competition `PL`
- Token in `.env` as `FOOTBALL_DATA_API_TOKEN`; never commit `.env`
- Cache API responses; do not call the live API from tests — mock responses instead

## Docs

- Humans: [README.md](README.md)
- Scope: [_docs/specs.md](_docs/specs.md)
