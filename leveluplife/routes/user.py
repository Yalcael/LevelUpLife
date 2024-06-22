from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from leveluplife.controllers.user import UserController
from leveluplife.dependencies import get_user_controller
from leveluplife.models.user import UserCreate, UserUpdate, UserUpdatePassword
from leveluplife.models.view import UserWithTask

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=UserWithTask, status_code=201)
async def create_user(
    *, user: UserCreate, user_controller: UserController = Depends(get_user_controller)
) -> UserWithTask:
    return UserWithTask.model_validate(await user_controller.create_user(user))


@router.get("/", response_model=Sequence[UserWithTask])
async def get_users(
    *, offset: int = 0, user_controller: UserController = Depends(get_user_controller)
) -> Sequence[UserWithTask]:
    return [
        UserWithTask.model_validate(user)
        for user in await user_controller.get_users(offset * 20, 20)
    ]


@router.get("/{user_id}", response_model=UserWithTask)
async def get_user_by_id(
    *, user_id: UUID, user_controller: UserController = Depends(get_user_controller)
) -> UserWithTask:
    return UserWithTask.model_validate(await user_controller.get_user_by_id(user_id))


@router.get("/type/username", response_model=UserWithTask)
async def get_user_by_username(
    *,
    user_username: str,
    user_controller: UserController = Depends(get_user_controller),
) -> UserWithTask:
    return UserWithTask.model_validate(
        await user_controller.get_user_by_username(user_username)
    )


@router.get("/type/email", response_model=UserWithTask)
async def get_user_by_email(
    *, user_email: str, user_controller: UserController = Depends(get_user_controller)
) -> UserWithTask:
    return UserWithTask.model_validate(
        await user_controller.get_user_by_email(user_email)
    )


@router.get("/type/tribe", response_model=Sequence[UserWithTask])
async def get_users_by_tribe(
    *,
    offset: int = 0,
    user_tribe: str,
    user_controller: UserController = Depends(get_user_controller),
) -> Sequence[UserWithTask]:
    users = await user_controller.get_users_by_tribe(user_tribe, offset * 20, 20)
    return [UserWithTask.model_validate(user) for user in users]


@router.patch("/{user_id}", response_model=UserWithTask)
async def update_user(
    *,
    user_id: UUID,
    user_update: UserUpdate,
    user_controller: UserController = Depends(get_user_controller),
) -> UserWithTask:
    return UserWithTask.model_validate(
        await user_controller.update_user(user_id, user_update)
    )


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    *, user_id: UUID, user_controller: UserController = Depends(get_user_controller)
) -> None:
    await user_controller.delete_user(user_id)


@router.patch("/{user_id}/password", response_model=UserWithTask)
async def update_user_password(
    *,
    user_id: UUID,
    user_update_password: UserUpdatePassword,
    user_controller: UserController = Depends(get_user_controller),
) -> UserWithTask:
    return UserWithTask.model_validate(
        await user_controller.update_user_password(
            user_id, user_update_password.password
        )
    )
