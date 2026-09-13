# Premier League Scoreboard (`pl_scoreboard`)

## Purpose

Build a simple tool that shows the current Premier League table and this week's results and fixtures.

## Target Users

- Anyone who wants a quick view of the league
- Shared device or personal browser
- No accounts or login required

## Core Features

1. Show the current league table
	- Rank, club, played, wins, draws, losses
	- Goals for, goals against, goal difference, points
	- Current Premier League season only

2. Show this week's matches
	- Finished matches with scores
	- Upcoming matches with kickoff times
	- Same page as the table

3. Load live data on page open
	- Fetch standings and matches when the user opens the page
	- Use a short local cache so reloads do not always hit the API
	- No auto-refresh and no in-play minute or event updates

## Platform and Storage

- App name: `pl_scoreboard`; FastAPI app in `backend/`
- Local, mobile-friendly web app
- OpenAPI contract in `openapi.yaml`
- SQLAlchemy persistence; default SQLite, swap via `DATABASE_URL`
- Live football API (football-data.org, competition `PL`) later
- API key stored in `.env`, not committed

## Out of Scope for the MVP

- User accounts and authentication
- Auto-refresh, websockets, live match events
- Past seasons or a season picker
- Filter by club, last-5 form, club or squad pages
- Top scorers, cards, xG, or other extra stats
- Notifications, predictions, or fantasy features
- Manual result entry

## MVP Success Criteria

- A visitor can open the app and see the current Premier League table.
- The same page shows this week's results and upcoming fixtures.
- Reloading the page can use cached data if the last fetch is still fresh.
- Tests pass without calling the live API.
