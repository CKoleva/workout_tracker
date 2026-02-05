from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.database import Base


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    type = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    calories = Column(Integer, nullable=False)

    date = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="workouts")