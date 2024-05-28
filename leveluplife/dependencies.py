from fastapi import Depends
from sqlmodel import Session

from leveluplife.controllers.user import UserController
from leveluplife.database import create_app_engine


def get_session():
    engine = create_app_engine()
    with Session(engine) as session:
        yield session


def get_user_controller(session: Session = Depends(get_session)) -> UserController:
    return UserController(session)
