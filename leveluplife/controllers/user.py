from typing import Sequence
from uuid import UUID

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select

from leveluplife.models.error import UserAlreadyExistsError, UserNotFoundError
from leveluplife.models.user import UserCreate, User, Tribe


class UserController:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def create_user(self, user_create: UserCreate) -> User:
        try:
            initial_stats = self.calculate_initial_stats(user_create.tribe)

            new_user = User(**user_create.dict(), **initial_stats)
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            return new_user
        except IntegrityError:
            raise UserAlreadyExistsError(email=user_create.email)

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
        return self.session.exec(select(User)).all()

    async def get_user_by_id(self, user_id: UUID) -> User:
        try:
            return self.session.exec(select(User).where(User.id == user_id)).one()
        except NoResultFound:
            raise UserNotFoundError(user_id=user_id)
