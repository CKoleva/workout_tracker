from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WorkoutBase(BaseModel):
    type: str
    duration: int
    calories: int
    date: datetime | None = None


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutRead(WorkoutBase):
    id: int

    model_config = ConfigDict(from_attributes=True)