from pydantic import BaseModel


class SummaryRead(BaseModel):
    total_workouts: int
    total_duration: int
    total_calories: int