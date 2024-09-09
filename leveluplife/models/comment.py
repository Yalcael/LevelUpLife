from uuid import UUID

from sqlmodel import Field

from leveluplife.models.shared import DBModel


class CommentBase(DBModel):
    content: str = None
    user_id: UUID | None = Field(foreign_key="user.id")
    task_id: UUID | None = Field(foreign_key="task.id")


class CommentCreate(CommentBase):
    pass


class CommentUpdate(DBModel):
    content: str | None = None
