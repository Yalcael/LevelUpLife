import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from leveluplife.dependencies import get_item_controller
from leveluplife.controllers.item import ItemController
from leveluplife.models.error import ItemAlreadyExistsError
from leveluplife.models.table import Item


@pytest.mark.asyncio
async def test_create_item(
    item_controller: ItemController, app: FastAPI, client: TestClient
) -> None:
    item_data = {
        "name": "JohnDoe",
        "description": "description test",
        "price_sell": "100",
        "strength": "10",
        "intelligence": "10",
        "agility": "10",
        "wise": "10",
        "psycho": "10",
    }

    mock_item = Item(
        id=uuid.uuid4(),
        created_at=datetime(2020, 1, 1),
        updated_at=datetime(2021, 1, 1),
        deleted_at=None,
        **item_data,
    )

    def _mock_create_item():
        item_controller.create_item = AsyncMock(return_value=mock_item)
        return item_controller

    app.dependency_overrides[get_item_controller] = _mock_create_item

    create_item_response = client.post("/items", json=item_data)
    assert create_item_response.status_code == 201
    actual_response = create_item_response.json()
    assert actual_response == {
        "id": str(mock_item.id),
        "created_at": mock_item.created_at.isoformat(),
        "updated_at": mock_item.updated_at.isoformat(),
        "deleted_at": None,
        "name": mock_item.name,
        "description": mock_item.description,
        "price_sell": mock_item.price_sell,
        "agility": mock_item.agility,
        "intelligence": mock_item.intelligence,
        "psycho": mock_item.psycho,
        "strength": mock_item.strength,
        "wise": mock_item.wise,
    }


@pytest.mark.asyncio
async def test_create_item_raise_item_already_exists_error(
    item_controller: ItemController, app: FastAPI, client: TestClient
):
    item_data = {
        "name": "JohnDoe",
        "description": "description test",
        "price_sell": "100",
        "strength": "10",
        "intelligence": "10",
        "agility": "10",
        "wise": "10",
        "psycho": "10",
    }

    def _mock_create_item():
        item_controller.create_item = AsyncMock(
            side_effect=ItemAlreadyExistsError(_name=item_data["name"])
        )
        return item_controller

    app.dependency_overrides[get_item_controller] = _mock_create_item

    create_item_response = client.post("/items", json=item_data)
    assert create_item_response.status_code == 409
    assert create_item_response.json() == {
        "name": "ItemAlreadyExistsError",
        "message": f"Item with the name {item_data['name']} already exists.",
        "status_code": 409,
    }


@pytest.mark.asyncio
async def test_get_items(
    item_controller: ItemController, client: TestClient, app: FastAPI
) -> None:
    mock_items = [
        Item(
            id=uuid.uuid4(),
            created_at=datetime(2020, 1, 1),
            updated_at=datetime(2021, 1, 1),
            deleted_at=None,
            name="JohnDoe",
            description="John Doe is going to the supermarket",
            price_sell=100,
            strength=10,
            intelligence=10,
            agility=10,
            wise=10,
            psycho=10,
        ),
        Item(
            id=uuid.uuid4(),
            created_at=datetime(2020, 1, 1),
            updated_at=datetime(2021, 1, 1),
            deleted_at=None,
            name="JohnDoe2",
            description="John Doe is going to the supermarket",
            price_sell=100,
            strength=10,
            intelligence=10,
            agility=10,
            wise=10,
            psycho=10,
        ),
    ]

    def _mock_get_items():
        item_controller.get_items = AsyncMock(return_value=mock_items)
        return item_controller

    app.dependency_overrides[get_item_controller] = _mock_get_items

    get_item_response = client.get("/items")
    assert get_item_response.status_code == 200
    assert get_item_response.json() == [
        {
            "id": str(item.id),
            "created_at": item.created_at.isoformat(),
            "updated_at": item.updated_at.isoformat(),
            "deleted_at": None,
            "name": item.name,
            "description": item.description,
            "price_sell": item.price_sell,
            "strength": item.strength,
            "intelligence": item.intelligence,
            "agility": item.agility,
            "wise": item.wise,
            "psycho": item.psycho,
            "users": [],
        }
        for item in mock_items
    ]
