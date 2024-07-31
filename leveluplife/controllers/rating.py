from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session

from leveluplife.models.error import RatingAlreadyExistsError, UserNotFoundError
from leveluplife.models.rating import RatingCreate
from leveluplife.models.table import Rating


class RatingController:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def create_rating(self, rating_create: RatingCreate) -> Rating:
        try:
            new_rating = Rating(**rating_create.model_dump())
            self.session.add(new_rating)
            self.session.commit()
            self.session.refresh(new_rating)
            return new_rating
        except NoResultFound:
            raise UserNotFoundError(user_id=rating_create.user_id)
        except IntegrityError:
            self.session.rollback()
            raise RatingAlreadyExistsError(task_id=rating_create.task_id)
