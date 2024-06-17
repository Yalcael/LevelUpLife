from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from leveluplife.models.task import TaskBase
from leveluplife.models.user import UserBase


class User(UserBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    strength: int = 0
    intelligence: int = 0
    agility: int = 0
    wise: int = 0
    psycho: int = 0
    experience: int = 0
    password: str = Field(min_length=4)
    tasks: list["Task"] = Relationship(back_populates="user")


class Task(TaskBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    user: User | None = Relationship(back_populates="tasks")
