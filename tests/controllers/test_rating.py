import pytest
from faker import Faker
from sqlmodel import Session, select

from leveluplife.controllers.rating import RatingController
from leveluplife.controllers.task import TaskController
from leveluplife.controllers.user import UserController
from leveluplife.models.error import RatingAlreadyExistsError
from leveluplife.models.rating import RatingCreate
from leveluplife.models.table import Rating
from leveluplife.models.task import TaskCreate
from leveluplife.models.user import Tribe, UserCreate


@pytest.mark.asyncio
async def test_create_rating(
    task_controller: TaskController,
    user_controller: UserController,
    rating_controller: RatingController,
    session: Session,
    faker: Faker,
) -> None:
    # Prepare
    user_create = UserCreate(
        username=faker.unique.user_name(),
        email=faker.unique.email(),
        password=faker.password(),
        tribe=Tribe.NOSFERATI,
    )
    user = await user_controller.create_user(user_create)

    task_create = TaskCreate(
        title=faker.unique.word(),
        description=faker.text(max_nb_chars=400),
        completed=faker.boolean(),
        category=faker.word(),
        user_id=user.id,
    )
    task = await task_controller.create_task(task_create)

    rating_create = RatingCreate(
        task_id=task.id,
        user_id=user.id,
        rating=faker.random_int(min=0, max=10),
    )

    # Act
    result = await rating_controller.create_rating(rating_create)

    rating = session.exec(select(Rating).where(Rating.id == result.id)).one()

    # Assert
    assert result.rating == rating_create.rating == rating.rating
    assert result.task_id == rating_create.task_id == rating.task_id
    assert result.user_id == rating_create.user_id == rating.user_id


@pytest.mark.asyncio
async def test_create_rating_already_exists_error(
    task_controller: TaskController,
    user_controller: UserController,
    rating_controller: RatingController,
    faker: Faker,
) -> None:
    user_create = UserCreate(
        username=faker.unique.user_name(),
        email=faker.unique.email(),
        password=faker.password(),
        tribe=Tribe.NOSFERATI,
    )
    user = await user_controller.create_user(user_create)

    task_create = TaskCreate(
        title=faker.unique.word(),
        description=faker.text(max_nb_chars=400),
        completed=faker.boolean(),
        category=faker.word(),
        user_id=user.id,
    )
    task = await task_controller.create_task(task_create)

    rating_create = RatingCreate(
        task_id=task.id,
        user_id=user.id,
        rating=faker.random_int(min=0, max=10),
    )

    # Act
    await rating_controller.create_rating(rating_create)

    # Assert
    with pytest.raises(RatingAlreadyExistsError):
        await rating_controller.create_rating(rating_create)
