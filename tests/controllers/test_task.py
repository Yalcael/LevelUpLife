import pytest
from faker import Faker
from sqlmodel import Session, select
from leveluplife.controllers.task import TaskController
from leveluplife.models.error import TaskAlreadyExistsError
from leveluplife.models.task import TaskCreate, Task


@pytest.mark.asyncio
async def test_create_task(
    task_controller: TaskController, session: Session, faker: Faker
) -> None:
    # Prepare
    task_create = TaskCreate(
        title=faker.unique.word(),
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


@pytest.mark.asyncio
async def test_create_task_already_exists_error(
    task_controller: TaskController, faker: Faker
) -> None:
    task_create = TaskCreate(
        title=faker.unique.word(),
        description=faker.text(max_nb_chars=400),
        completed=faker.boolean(),
        category=faker.word(),
    )

    # Act
    await task_controller.create_task(task_create)

    # Assert
    with pytest.raises(TaskAlreadyExistsError):
        await task_controller.create_task(task_create)


@pytest.mark.asyncio
async def test_get_tasks(task_controller: TaskController, faker: Faker) -> None:
    number_tasks = 5
    created_tasks = []
    for _ in range(number_tasks):
        task_create = TaskCreate(
            title=faker.unique.word(),
            description=faker.text(max_nb_chars=400),
            completed=faker.boolean(),
            category=faker.word(),
        )
        created_task = await task_controller.create_task(task_create)
        created_tasks.append(created_task)

    all_tasks = await task_controller.get_tasks()

    assert len(all_tasks) == number_tasks

    for i, created_task in enumerate(created_tasks):
        assert all_tasks[i].title == created_task.title
        assert all_tasks[i].description == created_task.description
        assert all_tasks[i].completed == created_task.completed
        assert all_tasks[i].category == created_task.category
