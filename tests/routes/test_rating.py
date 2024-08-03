import uuid
from datetime import datetime
from unittest.mock import AsyncMock
from leveluplife.dependencies import get_rating_controller
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from leveluplife.controllers.rating import RatingController
from leveluplife.models.table import Rating


@pytest.mark.asyncio
async def test_create_rating(
    rating_controller: RatingController, app: FastAPI, client: TestClient
) -> None:
    rating_data = {
        "rating": 5,
        "user_id": str(uuid.uuid4()),
        "task_id": str(uuid.uuid4()),
    }

    mock_rating = Rating(
        id=uuid.uuid4(),
        created_at=datetime(2020, 1, 1),
        **rating_data,
    )

    def _mock_create_rating():
        rating_controller.create_rating = AsyncMock(return_value=mock_rating)
        return rating_controller

    app.dependency_overrides[get_rating_controller] = _mock_create_rating

    create_rating_response = client.post("/ratings", json=rating_data)
    assert create_rating_response.status_code == 201
    assert create_rating_response.json() == {
        "id": str(mock_rating.id),
        "created_at": mock_rating.created_at.isoformat(),
        "rating": mock_rating.rating,
        "user_id": str(mock_rating.user_id),
        "task_id": str(mock_rating.task_id),
    }
