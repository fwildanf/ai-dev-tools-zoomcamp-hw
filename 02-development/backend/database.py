import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from backend.models import Base

_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def database_url() -> str:
    return os.environ.get("DATABASE_URL", "sqlite:///./pl_scoreboard.db")


def _connect_args(url: str) -> dict:
    if url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(database_url(), connect_args=_connect_args(database_url()))
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)
    return _SessionLocal


def get_session() -> Generator[Session, None, None]:
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def reset_engine() -> None:
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionLocal = None


def init_db() -> None:
    from backend.repository import seed_if_empty

    Base.metadata.create_all(get_engine())
    if os.environ.get("SCOREBOARD_SEED", "1") == "0":
        return
    session = get_session_factory()()
    try:
        seed_if_empty(session)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
