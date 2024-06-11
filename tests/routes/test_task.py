import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from leveluplife.controllers.task import TaskController
from leveluplife.dependencies import get_task_controller
from leveluplife.models.error import TaskAlreadyExistsError
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


@pytest.mark.asyncio
async def test_create_task_raise_task_already_exists_error(
    task_controller: TaskController, client: TestClient, app: FastAPI
) -> None:
    task_data = {
        "title": "Supermarket",
        "description": "John Doe is going to the supermarket",
        "completed": "False",
        "category": "Groceries",
    }

    def _mock_create_task():
        task_controller.create_task = AsyncMock(
            side_effect=TaskAlreadyExistsError(title=task_data["title"])
        )
        return task_controller

    app.dependency_overrides[get_task_controller] = _mock_create_task

    create_task_response = client.post("/tasks", json=task_data)
    assert create_task_response.status_code == 409
    assert create_task_response.json() == {
        "name": "TaskAlreadyExistsError",
        "message": f"Task with the title {task_data['title']} already exists.",
        "status_code": 409,
    }


@pytest.mark.asyncio
async def test_get_tasks(
    task_controller: TaskController, client: TestClient, app: FastAPI
) -> None:
    mock_tasks = [
        Task(
            id=uuid.uuid4(),
            created_at=datetime(2020, 1, 1),
            title="Supermarket",
            description="John Doe is going to the supermarket",
            completed=False,
            category="Groceries",
        ),
        Task(
            id=uuid.uuid4(),
            created_at=datetime(2022, 2, 2),
            title="Video games",
            description="Playing video games",
            completed=True,
            category="Fun",
        ),
    ]

    def _mock_get_tasks():
        task_controller.get_tasks = AsyncMock(return_value=mock_tasks)
        return task_controller

    app.dependency_overrides[get_task_controller] = _mock_get_tasks

    get_task_response = client.get("/tasks")
    assert get_task_response.status_code == 200
    assert get_task_response.json() == [
        {
            "id": str(task.id),
            "created_at": task.created_at.isoformat(),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "category": task.category,
        }
        for task in mock_tasks
    ]
