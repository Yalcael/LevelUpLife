from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field

from leveluplife.models.shared import DBModel


class ItemBase(DBModel):
    name: str = Field(unique=True, index=True)
    description: str = Field(max_length=300)
    price_sell: int | None = None
    strength: int | None = None
    intelligence: int | None = None
    agility: int | None = None
    wise: int | None = None
    psycho: int | None = None


class Item(ItemBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime | None = Field(default=None)
    deleted_at: datetime | None = Field(default=None)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(DBModel):
    name: str | None = None
    description: str | None = None
    price_sell: int | None = None
    strength: int | None = None
    intelligence: int | None = None
    agility: int | None = None
    wise: int | None = None
    psycho: int | None = None
