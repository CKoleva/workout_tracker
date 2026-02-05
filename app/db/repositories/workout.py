from datetime import datetime
from sqlalchemy.orm import Session

from app.db.models.workout import Workout


def create_workout(
    db: Session,
    user_id: int,
    type: str,
    duration: int,
    calories: int,
    date=None,
) -> Workout:
    workout = Workout(
        user_id=user_id,
        type=type,
        duration=duration,
        calories=calories,
        date=date,
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


def list_workouts_for_user(db: Session, user_id: int) -> list[Workout]:
    return db.query(Workout).filter(Workout.user_id == user_id).all()

def list_workouts_for_user_in_period(
    db: Session,
    user_id: int,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
) -> list[Workout]:
    query = db.query(Workout).filter(Workout.user_id == user_id)

    if from_date is not None:
        query = query.filter(Workout.date >= from_date)

    if to_date is not None:
        query = query.filter(Workout.date <= to_date)

    return query.all()