from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.deps import get_db
from app.db.repositories.workout import get_workout_summary
from app.schemas.dashboard import SummaryRead

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=SummaryRead)
def summary(
    from_date: datetime | None = Query(default=None),
    to_date: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> SummaryRead:
    total_workouts, total_duration, total_calories = get_workout_summary(
        db=db,
        user_id=current_user.id,
        from_date=from_date,
        to_date=to_date,
    )
    return SummaryRead(
        total_workouts=total_workouts,
        total_duration=total_duration,
        total_calories=total_calories,
    )