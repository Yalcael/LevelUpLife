import pytest
from faker import Faker
from sqlmodel import select, Session

from leveluplife.controllers.item import ItemController
from leveluplife.models.error import ItemAlreadyExistsError
from leveluplife.models.item import ItemCreate
from leveluplife.models.table import Item


@pytest.mark.asyncio
async def test_create_item(
    item_controller: ItemController, session: Session, faker: Faker
) -> None:
    item_create = ItemCreate(
        name=faker.unique.word(),
        description=faker.text(max_nb_chars=300),
        price_sell=faker.random_int(min=0, max=100),
        strength=faker.random_int(min=0, max=100),
        intelligence=faker.random_int(min=0, max=100),
        agility=faker.random_int(min=0, max=100),
        wise=faker.random_int(min=0, max=100),
        psycho=faker.random_int(min=0, max=100),
    )
    # Act
    result = await item_controller.create_item(item_create)

    item = session.exec(select(Item).where(Item.id == result.id)).one()

    # Assert
    assert result.name == item_create.name == item.name
    assert result.description == item_create.description == item.description
    assert result.price_sell == item_create.price_sell == item.price_sell
    assert result.strength == item_create.strength == item.strength
    assert result.intelligence == item_create.intelligence == item.intelligence
    assert result.agility == item_create.agility == item.agility
    assert result.wise == item_create.wise == item.wise
    assert result.psycho == item_create.psycho == item.psycho


@pytest.mark.asyncio
async def test_create_item_already_exists_error(
    item_controller: ItemController, faker: Faker
) -> None:
    # Prepare
    item_create = ItemCreate(
        name=faker.unique.word(),
        description=faker.text(max_nb_chars=300),
        price_sell=faker.random_int(min=0, max=100),
        strength=faker.random_int(min=0, max=100),
        intelligence=faker.random_int(min=0, max=100),
        agility=faker.random_int(min=0, max=100),
        wise=faker.random_int(min=0, max=100),
        psycho=faker.random_int(min=0, max=100),
    )
    await item_controller.create_item(item_create)

    # Act / Assert
    with pytest.raises(ItemAlreadyExistsError):
        await item_controller.create_item(item_create)
