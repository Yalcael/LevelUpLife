from typing import Sequence
from uuid import UUID

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select
from loguru import logger
from leveluplife.models.error import (
    RatingAlreadyExistsError,
    UserNotFoundError,
    RatingNotFoundError,
)
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

    async def get_ratings(self, offset: int, limit: int) -> Sequence[Rating]:
        logger.info("Getting ratings")
        return self.session.exec(select(Rating).offset(offset).limit(limit)).all()

    async def get_rating_by_id(self, rating_id: UUID) -> Rating:
        try:
            logger.info(f"Getting rating by id: {rating_id}")
            return self.session.exec(select(Rating).where(Rating.id == rating_id)).one()
        except NoResultFound:
            raise RatingNotFoundError(rating_id=rating_id)
