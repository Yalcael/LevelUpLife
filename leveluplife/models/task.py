from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field

from leveluplife.models.shared import DBModel


class TaskBase(DBModel):
    title: str = Field(default=None, max_length=69, index=True, unique=True)
    description: str = Field(max_length=400)
    completed: bool
    category: str


class Task(TaskBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class TaskCreate(TaskBase):
    pass


class TaskUpdate(DBModel):
    description: str | None = None
    completed: bool | None = None
    category: str | None = None
    title: str | None = None
