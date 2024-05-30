import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from leveluplife.controllers.user import UserController
from leveluplife.dependencies import get_user_controller
from leveluplife.models.error import UserAlreadyExistsError
from leveluplife.models.user import User, Tribe


@pytest.mark.asyncio
async def test_create_user(
    user_controller: UserController, app: FastAPI, client: TestClient
) -> None:
    user_data = {
        "username": "JohnDoe",
        "email": "john.doe@test.com",
        "password": "johndoepassword",
        "tribe": "Nosferati",
    }

    mock_user = User(
        id=uuid.uuid4(),
        created_at=datetime(2020, 1, 1),
        tribe=Tribe(user_data["tribe"]),
        **{k: v for k, v in user_data.items() if k != "tribe"},
    )

    def _mock_create_user():
        user_controller.create_user = AsyncMock(return_value=mock_user)
        return user_controller

    app.dependency_overrides[get_user_controller] = _mock_create_user

    create_user_response = client.post("/users", json=user_data)
    assert create_user_response.status_code == 201
    actual_response = create_user_response.json()
    assert actual_response == {
        "id": str(mock_user.id),
        "created_at": mock_user.created_at.isoformat(),
        "username": mock_user.username,
        "email": mock_user.email,
        "tribe": mock_user.tribe.value,
        "agility": mock_user.agility,
        "background_image": mock_user.background_image,
        "biography": mock_user.biography,
        "experience": mock_user.experience,
        "intelligence": mock_user.intelligence,
        "profile_picture": mock_user.profile_picture,
        "psycho": mock_user.psycho,
        "strength": mock_user.strength,
        "wise": mock_user.wise,
    }


@pytest.mark.asyncio
async def test_create_user_raise_user_already_exists_error(
    user_controller: UserController, client: TestClient, app: FastAPI
) -> None:
    user_data = {
        "username": "JohnDoe",
        "email": "john.doe@test.com",
        "password": "johndoepassword",
        "tribe": "Nosferati",
    }

    def _mock_create_user():
        user_controller.create_user = AsyncMock(
            side_effect=UserAlreadyExistsError(email=user_data["email"])
        )
        return user_controller

    app.dependency_overrides[get_user_controller] = _mock_create_user

    create_user_response = client.post("/users", json=user_data)
    assert create_user_response.status_code == 409
    assert create_user_response.json() == {
        "name": "UserAlreadyExistsError",
        "message": f"User with the email {user_data['email']} already exists.",
        "status_code": 409,
    }


@pytest.mark.asyncio
async def test_get_users(
    user_controller: UserController, client: TestClient, app: FastAPI
) -> None:
    mock_users = [
        User(
            id=uuid.uuid4(),
            created_at=datetime(2020, 1, 1),
            tribe=Tribe("Nosferati"),
            username="JohnDoe",
            email="john.doe@test.com",
            password="johndoepassword",
        ),
        User(
            id=uuid.uuid4(),
            created_at=datetime(2022, 2, 2),
            tribe=Tribe("Saharans"),
            username="JaneDoe",
            email="jane.doe@test.com",
            password="janedoepassword",
        ),
    ]

    def _mock_get_users():
        user_controller.get_users = AsyncMock(return_value=mock_users)
        return user_controller

    app.dependency_overrides[get_user_controller] = _mock_get_users

    get_user_response = client.get("/users")
    assert get_user_response.status_code == 200
    assert get_user_response.json() == [
        {
            "id": str(user.id),
            "created_at": user.created_at.isoformat(),
            "tribe": user.tribe.value,
            "username": user.username,
            "email": user.email,
            "experience": user.experience,
            "biography": user.biography,
            "background_image": user.background_image,
            "profile_picture": user.profile_picture,
            "agility": user.agility,
            "intelligence": user.intelligence,
            "psycho": user.psycho,
            "strength": user.strength,
            "wise": user.wise,
        }
        for user in mock_users
    ]
