from fastapi import FastAPI

from app.db.database import engine, Base
from app.db import models


app = FastAPI(title="Workout Tracker")

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

