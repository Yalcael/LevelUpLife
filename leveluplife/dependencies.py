from fastapi import Depends
from sqlmodel import Session

from leveluplife.controllers.item import ItemController
from leveluplife.controllers.rating import RatingController
from leveluplife.controllers.task import TaskController
from leveluplife.controllers.user import UserController
from leveluplife.database import create_app_engine


def get_session():
    engine = create_app_engine()
    with Session(engine) as session:
        yield session


def get_user_controller(session: Session = Depends(get_session)) -> UserController:
    return UserController(session)


def get_task_controller(session: Session = Depends(get_session)) -> TaskController:
    return TaskController(session)


def get_item_controller(session: Session = Depends(get_session)) -> ItemController:
    return ItemController(session)


def get_rating_controller(session: Session = Depends(get_session)) -> RatingController:
    return RatingController(session)
