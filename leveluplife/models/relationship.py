from datetime import datetime
from uuid import UUID

from sqlmodel import Field

from leveluplife.models.shared import DBModel


class UserItemLink(DBModel, table=True):
    user_id: UUID | None = Field(foreign_key="user.id", primary_key=True)
    item_id: UUID | None = Field(foreign_key="item.id", primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    equipped: bool = Field(default=False)


class UserItemLinkCreate(DBModel):
    user_ids: list[UUID]
    equipped: bool = Field(default=False)
