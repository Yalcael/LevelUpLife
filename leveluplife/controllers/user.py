from typing import Sequence
from uuid import UUID
from loguru import logger
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select

from leveluplife.models.error import (
    UserNotFoundError,
    UserEmailAlreadyExistsError,
    UserUsernameAlreadyExistsError,
)
from leveluplife.models.table import User
from leveluplife.models.user import UserCreate, Tribe, UserUpdate


class UserController:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def create_user(self, user_create: UserCreate) -> User:
        try:
            # Calculate initial stats based on the tribe
            initial_stats = self.calculate_initial_stats(user_create.tribe)

            # Create new user
            new_user = User(**user_create.dict(), **initial_stats)
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            logger.info(f"New user created: {new_user.username}")
            return new_user

        except IntegrityError:
            self.session.rollback()
            existing_user_by_email = self.session.exec(
                select(User).where(User.email == user_create.email)
            ).first()
            if existing_user_by_email:
                raise UserEmailAlreadyExistsError(email=user_create.email)
            existing_user_by_username = self.session.exec(
                select(User).where(User.username == user_create.username)
            ).first()
            if existing_user_by_username:
                raise UserUsernameAlreadyExistsError(username=user_create.username)

    @staticmethod
    def calculate_initial_stats(tribe: Tribe) -> dict[str, int]:
        if tribe == Tribe.NOSFERATI:
            return {
                "intelligence": 8,
                "strength": 2,
                "agility": 2,
                "wise": 1,
                "psycho": 10,
            }
        elif tribe == Tribe.VALHARS:
            return {
                "intelligence": 1,
                "strength": 10,
                "agility": 6,
                "wise": 6,
                "psycho": 2,
            }
        elif tribe == Tribe.SAHARANS:
            return {
                "intelligence": 9,
                "strength": 2,
                "agility": 3,
                "wise": 10,
                "psycho": 1,
            }
        elif tribe == Tribe.GLIMMERKINS:
            return {
                "intelligence": 10,
                "strength": 2,
                "agility": 2,
                "wise": 7,
                "psycho": 4,
            }
        else:
            return {
                "intelligence": 5,
                "strength": 5,
                "agility": 5,
                "wise": 5,
                "psycho": 5,
            }

    async def get_users(self) -> Sequence[User]:
        logger.info("Getting users")
        return self.session.exec(select(User)).all()

    async def get_user_by_id(self, user_id: UUID) -> User:
        try:
            logger.info("Getting user by id")
            return self.session.exec(select(User).where(User.id == user_id)).one()
        except NoResultFound:
            raise UserNotFoundError(user_id=user_id)

    async def update_user(self, user_id: UUID, user_update: UserUpdate) -> User:
        try:
            db_user = self.session.exec(select(User).where(User.id == user_id)).one()
            db_user_data = user_update.model_dump(exclude_unset=True)
            db_user.sqlmodel_update(db_user_data)
            self.session.add(db_user)
            self.session.commit()
            self.session.refresh(db_user)
            logger.info(f"Updated user: {db_user.username}")
            return db_user
        except NoResultFound:
            raise UserNotFoundError(user_id=user_id)

    async def delete_user(self, user_id: UUID) -> None:
        try:
            db_user = self.session.exec(select(User).where(User.id == user_id)).one()
            self.session.delete(db_user)
            self.session.commit()
        except NoResultFound:
            raise UserNotFoundError(user_id=user_id)

    async def update_user_password(self, user_id: UUID, password: str) -> User:
        try:
            db_user = self.session.exec(select(User).where(User.id == user_id)).one()
            db_user.password = password
            self.session.add(db_user)
            self.session.commit()
            self.session.refresh(db_user)
            logger.info(f"Updated user password: {db_user.username}")
            return db_user
        except NoResultFound:
            raise UserNotFoundError(user_id=user_id)
