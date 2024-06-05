import pytest
from faker import Faker
from sqlmodel import Session, select

from leveluplife.controllers.task import TaskController
from leveluplife.models.task import TaskCreate, Task


@pytest.mark.asyncio
async def test_create_task(
    task_controller: TaskController, session: Session, faker: Faker
) -> None:
    # Prepare
    task_create = TaskCreate(
        title=faker.word(),
        description=faker.text(max_nb_chars=400),
        completed=faker.boolean(),
        category=faker.word(),
    )
    # Act
    result = await task_controller.create_task(task_create)

    task = session.exec(select(Task).where(Task.id == result.id)).one()

    # Assert
    assert result.title == task_create.title == task.title
    assert result.description == task_create.description == task.description
    assert result.completed == task_create.completed == task.completed
    assert result.category == task_create.category == task.category
