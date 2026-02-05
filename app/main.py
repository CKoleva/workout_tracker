from fastapi import FastAPI

from app.db.database import engine, Base
from app.db import models
from app.api.auth import router as auth_router
from app.api import workouts


app = FastAPI(title="Workout Tracker")
app.include_router(auth_router)
app.include_router(workouts.router)

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

