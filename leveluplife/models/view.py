from datetime import datetime
from uuid import UUID

from leveluplife.models.item import ItemBase
from leveluplife.models.relationship import UserItemLink
from leveluplife.models.task import TaskBase
from leveluplife.models.user import UserBase


class UserView(UserBase):
    id: UUID
    created_at: datetime
    strength: int = 0
    intelligence: int = 0
    agility: int = 0
    wise: int = 0
    psycho: int = 0
    experience: int = 0
    items: list["UserItemLink"] = []


class TaskView(TaskBase):
    id: UUID
    created_at: datetime


class ItemView(ItemBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    items: list["UserItemLink"] = []


class UserWithTask(UserView):
    tasks: list["TaskView"] = []


class TaskWithUser(TaskView):
    user: "UserView"
