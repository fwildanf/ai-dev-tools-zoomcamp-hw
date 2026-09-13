from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend import db
from backend.schemas import Error, Health, Match, Scoreboard

FRONTENT_DIR = Path(__file__).resolve().parent.parent / "frontent"

app = FastAPI(
    title="Premier League Scoreboard API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health", response_model=Health)
def get_health() -> Health:
    return Health(status="ok")


@app.get("/api/scoreboard", response_model=Scoreboard)
def get_scoreboard() -> Scoreboard:
    return Scoreboard.model_validate(db.get_scoreboard())


@app.get(
    "/api/matches/{match_id}",
    response_model=Match,
    responses={404: {"model": Error}},
)
def get_match(match_id: str) -> Match:
    match = db.get_match(match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return Match.model_validate(match)


@app.get("/")
def frontend_index() -> FileResponse:
    return FileResponse(FRONTENT_DIR / "index.html")


app.mount("/css", StaticFiles(directory=FRONTENT_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTENT_DIR / "js"), name="js")
