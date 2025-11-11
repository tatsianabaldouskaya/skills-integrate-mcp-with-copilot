from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime


class ActivityParticipant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_id: int = Field(foreign_key="activity.id")
    email: str
    signed_up_at: datetime = Field(default_factory=datetime.utcnow)


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    schedule: Optional[str] = None
    max_participants: Optional[int] = None

    participants: List[ActivityParticipant] = Relationship(back_populates="activity")


# Back-populate relationship on the join table
ActivityParticipant.activity = Relationship(back_populates="participants")
