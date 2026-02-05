from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.deps import get_db
from app.db.repositories.workout import create_workout, list_workouts_for_user
from app.schemas.workout import WorkoutCreate, WorkoutRead

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/", response_model=WorkoutRead)
def create_new_workout(
    payload: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_workout(
        db=db,
        user_id=current_user.id,
        type=payload.type,
        duration=payload.duration,
        calories=payload.calories,
        date=payload.date,
    )


@router.get("/", response_model=list[WorkoutRead])
def list_my_workouts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return list_workouts_for_user(db, current_user.id)