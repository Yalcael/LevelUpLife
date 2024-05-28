from fastapi import APIRouter, Depends

from leveluplife.controllers.user import UserController
from leveluplife.dependencies import get_user_controller
from leveluplife.models.user import UserCreate
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
