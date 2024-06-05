import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from leveluplife.controllers.task import TaskController
from leveluplife.dependencies import get_task_controller
from leveluplife.models.task import Task


@pytest.mark.asyncio
async def test_create_test(
    task_controller: TaskController, app: FastAPI, client: TestClient
) -> None:
    task_data = {
        "title": "Supermarket",
        "description": "John Doe is going to the supermarket",
        "completed": "False",
        "category": "Groceries",
    }

    mock_task = Task(
        id=uuid.uuid4(),
        created_at=datetime(2020, 1, 1),
        **task_data,
    )

    def _mock_create_task():
        task_controller.create_task = AsyncMock(return_value=mock_task)
        return task_controller

    app.dependency_overrides[get_task_controller] = _mock_create_task

    create_task_response = client.post("/tasks", json=task_data)
    assert create_task_response.status_code == 201
    assert create_task_response.json() == {
        "id": str(mock_task.id),
        "created_at": mock_task.created_at.isoformat(),
        "title": mock_task.title,
        "description": mock_task.description,
        "completed": mock_task.completed,
        "category": mock_task.category,
    }
