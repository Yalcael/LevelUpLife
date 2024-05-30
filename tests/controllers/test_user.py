import random

import pytest
from faker import Faker
from sqlmodel import Session, select

from leveluplife.controllers.user import UserController
from leveluplife.models.error import UserAlreadyExistsError, UserNotFoundError
from leveluplife.models.user import UserCreate, Tribe, User


# Dictionary of expected stats for each tribe
expected_stats = {
    "Nosferati": {
        "intelligence": 8,
        "strength": 2,
        "agility": 2,
        "wise": 1,
        "psycho": 10,
    },
    "Valhars": {
        "intelligence": 1,
        "strength": 10,
        "agility": 6,
        "wise": 6,
        "psycho": 2,
    },
    "Saharans": {
        "intelligence": 9,
        "strength": 2,
        "agility": 3,
        "wise": 10,
        "psycho": 1,
    },
    "Glimmerkins": {
        "intelligence": 10,
        "strength": 2,
        "agility": 2,
        "wise": 7,
        "psycho": 4,
    },
    "Neutrals": {
        "intelligence": 5,
        "strength": 5,
        "agility": 5,
        "wise": 5,
        "psycho": 5,
    },
}


@pytest.mark.asyncio
async def test_create_user_nosferati(
    user_controller: UserController, session: Session, faker: Faker
) -> None:
    # Prepare
    user_create = UserCreate(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
        tribe=Tribe("Nosferati"),
    )
    # Act
    result = await user_controller.create_user(user_create)

    user = session.exec(select(User).where(User.id == result.id)).one()

    # Assert
    assert result.username == user_create.username == user.username
    assert result.email == user_create.email == user.email
    assert result.password == user_create.password == user.password
    assert result.tribe == user_create.tribe == user.tribe
    assert result.intelligence == expected_stats["Nosferati"]["intelligence"]
    assert result.strength == expected_stats["Nosferati"]["strength"]
    assert result.agility == expected_stats["Nosferati"]["agility"]
    assert result.wise == expected_stats["Nosferati"]["wise"]
    assert result.psycho == expected_stats["Nosferati"]["psycho"]


@pytest.mark.asyncio
async def test_create_user_valhars(
    user_controller: UserController, session: Session, faker: Faker
) -> None:
    # Prepare
    user_create = UserCreate(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
        tribe=Tribe("Valhars"),
    )
    # Act
    result = await user_controller.create_user(user_create)

    user = session.exec(select(User).where(User.id == result.id)).one()

    # Assert
    assert result.username == user_create.username == user.username
    assert result.email == user_create.email == user.email
    assert result.password == user_create.password == user.password
    assert result.tribe == user_create.tribe == user.tribe
    assert result.intelligence == expected_stats["Valhars"]["intelligence"]
    assert result.strength == expected_stats["Valhars"]["strength"]
    assert result.agility == expected_stats["Valhars"]["agility"]
    assert result.wise == expected_stats["Valhars"]["wise"]
    assert result.psycho == expected_stats["Valhars"]["psycho"]


@pytest.mark.asyncio
async def test_create_user_saharans(
    user_controller: UserController, session: Session, faker: Faker
) -> None:
    # Prepare
    user_create = UserCreate(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
        tribe=Tribe("Saharans"),
    )
    # Act
    result = await user_controller.create_user(user_create)

    user = session.exec(select(User).where(User.id == result.id)).one()

    # Assert
    assert result.username == user_create.username == user.username
    assert result.email == user_create.email == user.email
    assert result.password == user_create.password == user.password
    assert result.tribe == user_create.tribe == user.tribe
    assert result.intelligence == expected_stats["Saharans"]["intelligence"]
    assert result.strength == expected_stats["Saharans"]["strength"]
    assert result.agility == expected_stats["Saharans"]["agility"]
    assert result.wise == expected_stats["Saharans"]["wise"]
    assert result.psycho == expected_stats["Saharans"]["psycho"]


@pytest.mark.asyncio
async def test_create_user_glimmerkins(
    user_controller: UserController, session: Session, faker: Faker
) -> None:
    # Prepare
    user_create = UserCreate(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
        tribe=Tribe("Glimmerkins"),
    )
    # Act
    result = await user_controller.create_user(user_create)

    user = session.exec(select(User).where(User.id == result.id)).one()

    # Assert
    assert result.username == user_create.username == user.username
    assert result.email == user_create.email == user.email
    assert result.password == user_create.password == user.password
    assert result.tribe == user_create.tribe == user.tribe
    assert result.intelligence == expected_stats["Glimmerkins"]["intelligence"]
    assert result.strength == expected_stats["Glimmerkins"]["strength"]
    assert result.agility == expected_stats["Glimmerkins"]["agility"]
    assert result.wise == expected_stats["Glimmerkins"]["wise"]
    assert result.psycho == expected_stats["Glimmerkins"]["psycho"]


@pytest.mark.asyncio
async def test_create_user_neutrals(
    user_controller: UserController, session: Session, faker: Faker
) -> None:
    # Prepare
    user_create = UserCreate(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
        tribe=Tribe("Neutrals"),
    )
    # Act
    result = await user_controller.create_user(user_create)

    user = session.exec(select(User).where(User.id == result.id)).one()

    # Assert
    assert result.username == user_create.username == user.username
    assert result.email == user_create.email == user.email
    assert result.password == user_create.password == user.password
    assert result.tribe == user_create.tribe == user.tribe
    assert result.intelligence == expected_stats["Neutrals"]["intelligence"]
    assert result.strength == expected_stats["Neutrals"]["strength"]
    assert result.agility == expected_stats["Neutrals"]["agility"]
    assert result.wise == expected_stats["Neutrals"]["wise"]
    assert result.psycho == expected_stats["Neutrals"]["psycho"]


@pytest.mark.asyncio
async def test_create_user_already_exists_error(
    user_controller: UserController, faker: Faker
) -> None:
    user_create = UserCreate(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
        tribe=random.choice(list(Tribe)),
    )

    # Act
    await user_controller.create_user(user_create)

    # Assert
    with pytest.raises(UserAlreadyExistsError):
        await user_controller.create_user(user_create)


@pytest.mark.asyncio
async def test_get_users(user_controller: UserController, faker: Faker) -> None:
    number_users = 5
    created_users = []
    for _ in range(number_users):
        user_create = UserCreate(
            username=faker.user_name(),
            email=faker.email(),
            password=faker.password(),
            tribe=random.choice(list(Tribe)),
        )
        created_user = await user_controller.create_user(user_create)
        created_users.append(created_user)

    all_users = await user_controller.get_users()

    assert len(all_users) == number_users

    for i, created_user in enumerate(created_users):
        assert all_users[i].username == created_user.username
        assert all_users[i].email == created_user.email
        assert all_users[i].tribe == created_user.tribe
        assert all_users[i].intelligence == created_user.intelligence
        assert all_users[i].strength == created_user.strength
        assert all_users[i].agility == created_user.agility
        assert all_users[i].wise == created_user.wise
        assert all_users[i].psycho == created_user.psycho


@pytest.mark.asyncio
async def test_get_user_by_id(user_controller: UserController, faker: Faker) -> None:
    user_create = UserCreate(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
        tribe=random.choice(list(Tribe)),
    )

    created_user = await user_controller.create_user(user_create)

    retrieved_user = await user_controller.get_user_by_id(created_user.id)

    assert retrieved_user.id == created_user.id
    assert retrieved_user.username == user_create.username
    assert retrieved_user.email == user_create.email
    assert retrieved_user.tribe == user_create.tribe
    assert retrieved_user.password == user_create.password


@pytest.mark.asyncio
async def test_get_user_by_id_raise_user_not_found_error(
    user_controller: UserController, faker: Faker
) -> None:
    non_existent_user_id = faker.uuid4()
    with pytest.raises(UserNotFoundError):
        await user_controller.get_user_by_id(non_existent_user_id)
