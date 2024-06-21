from uuid import UUID, uuid4

from sqlmodel import Field

from leveluplife.models.shared import DBModel


class ItemBase(DBModel):
    name: str = Field(unique=True, index=True)
    description: str = Field(max_length=300)
    price_sell: int
    strength: int = 0
    intelligence: int = 0
    agility: int = 0
    wise: int = 0
    psycho: int = 0


class Item(ItemBase):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True, unique=True)


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
