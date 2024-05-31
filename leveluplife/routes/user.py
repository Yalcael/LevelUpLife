from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from leveluplife.controllers.user import UserController
from leveluplife.dependencies import get_user_controller
from leveluplife.models.user import UserCreate, UserUpdate
from leveluplife.models.view import UserView

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=UserView, status_code=201)
async def create_user(
    *, user: UserCreate, user_controller: UserController = Depends(get_user_controller)
) -> UserView:
    return UserView.model_validate(await user_controller.create_user(user))


@router.get("/", response_model=Sequence[UserView])
async def get_users(
    *, user_controller: UserController = Depends(get_user_controller)
) -> Sequence[UserView]:
    return [UserView.model_validate(user) for user in await user_controller.get_users()]


@router.get("/{user_id}", response_model=UserView)
async def get_user_by_id(
    *, user_id: UUID, user_controller: UserController = Depends(get_user_controller)
) -> UserView:
    return UserView.model_validate(await user_controller.get_user_by_id(user_id))


@router.patch("/{user_id}", response_model=UserView)
async def update_user(
    *,
    user_id: UUID,
    user_update: UserUpdate,
    user_controller: UserController = Depends(get_user_controller)
) -> UserView:
    return UserView.model_validate(
        await user_controller.update_user(user_id, user_update)
    )
