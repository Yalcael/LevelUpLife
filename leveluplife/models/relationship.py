from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field

from leveluplife.models.shared import DBModel


class UserItemLink(DBModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    user_id: UUID | None = Field(foreign_key="user.id", unique=True)
    item_id: UUID | None = Field(foreign_key="item.id", unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    equipped: bool = Field(default=False)
