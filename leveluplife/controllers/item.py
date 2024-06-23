from datetime import datetime
from typing import Sequence
from uuid import UUID

from loguru import logger
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select

from leveluplife.models.error import (
    ItemAlreadyExistsError,
    ItemNameNotFoundError,
    ItemNotFoundError,
)
from leveluplife.models.item import ItemCreate, ItemUpdate
from leveluplife.models.table import Item


class ItemController:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def create_item(self, item_create: ItemCreate) -> Item:
        try:
            new_item = Item(**item_create.dict())
            self.session.add(new_item)
            self.session.commit()
            self.session.refresh(new_item)
            logger.info(f"New item created: {new_item.name}")
            return new_item
        except IntegrityError:
            raise ItemAlreadyExistsError(_name=item_create.name)

    async def update_item(self, item_id: UUID, item_update: ItemUpdate) -> Item:
        try:
            db_item = self.session.exec(select(Item).where(Item.id == item_id)).one()
            db_item_data = item_update.model_dump(exclude_unset=True)
            db_item.sqlmodel_update(db_item_data)
            self.session.add(db_item)
            db_item.updated_at = datetime.now()
            self.session.commit()
            self.session.refresh(db_item)
            logger.info(f"Updated item: {db_item.name}")
            return db_item
        except NoResultFound:
            raise ItemNotFoundError(item_id=item_id)

    async def delete_item(self, item_id: UUID) -> None:
        try:
            db_item = self.session.exec(select(Item).where(Item.id == item_id)).one()
            self.session.delete(db_item)
            db_item.updated_at = datetime.now()
            self.session.commit()
            logger.info(f"Deleted item: {db_item.name}")
        except NoResultFound:
            raise ItemNotFoundError(item_id=item_id)

    async def get_items(self, offset: int, limit: int) -> Sequence[Item]:
        logger.info("Getting items")
        return self.session.exec(select(Item).offset(offset).limit(limit)).all()

    async def get_item_by_id(self, item_id: UUID) -> Item:
        try:
            logger.info(f"Getting item by id: {item_id}")
            return self.session.exec(select(Item).where(Item.id == item_id)).one()
        except NoResultFound:
            raise ItemNotFoundError(item_id=item_id)

    async def get_item_by_name(self, item_name: str) -> Item:
        try:
            logger.info(f"Getting item by name: {item_name}")
            return self.session.exec(select(Item).where(Item.name == item_name)).one()
        except NoResultFound:
            raise ItemNameNotFoundError(item_name=item_name)
