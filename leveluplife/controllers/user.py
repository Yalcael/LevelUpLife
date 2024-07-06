from uuid import UUID

from loguru import logger
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select

from leveluplife.models.error import (
    UserEmailAlreadyExistsError,
    UserEmailNotFoundError,
    UserNotFoundError,
    UserUsernameAlreadyExistsError,
    UserUsernameNotFoundError,
    ItemLinkToUserNotFoundError,
)
from leveluplife.models.relationship import UserItemLink
from leveluplife.models.table import User, Item, Task
from leveluplife.models.user import Tribe, UserCreate, UserUpdate
from leveluplife.models.view import TaskView, UserView, ItemUserView


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

    async def get_users(self, offset: int, limit: int) -> list[UserView]:
        logger.info("Getting users")
        user_with_items = self.session.exec(
            select(User, UserItemLink, Item, Task)
            .join(UserItemLink, User.id == UserItemLink.user_id, isouter=True)
            .join(Item, UserItemLink.item_id == Item.id, isouter=True)
            .join(Task, User.id == Task.user_id, isouter=True)
            .order_by(User.username)
            .offset(offset)
            .limit(limit)
        ).all()
        return self._construct_user_views(user_with_items)

    async def get_user_by_username(self, user_username: str) -> UserView:
        logger.info(f"Getting user by username: {user_username}")
        user_with_items = self.session.exec(
            select(User, UserItemLink, Item)
            .join(UserItemLink, User.id == UserItemLink.user_id, isouter=True)
            .join(Item, UserItemLink.item_id == Item.id, isouter=True)
            .where(User.username == user_username)
        ).all()
        if not user_with_items:
            raise UserUsernameNotFoundError(user_username=user_username)
        return self._construct_user_view(user_with_items)

    async def get_user_by_email(self, user_email: str) -> UserView:
        logger.info(f"Getting user by email: {user_email}")
        user_with_items = self.session.exec(
            select(User, UserItemLink, Item)
            .join(UserItemLink, User.id == UserItemLink.user_id, isouter=True)
            .join(Item, UserItemLink.item_id == Item.id, isouter=True)
            .where(User.email == user_email)
        ).all()
        if not user_with_items:
            raise UserEmailNotFoundError(user_email=user_email)
        return self._construct_user_view(user_with_items)

    async def get_users_by_tribe(
        self, user_tribe: Tribe, offset: int, limit: int
    ) -> list[UserView]:
        logger.info(f"Getting users by tribe: {user_tribe}")
        user_with_items = self.session.exec(
            select(User, UserItemLink, Item, Task)
            .join(UserItemLink, User.id == UserItemLink.user_id, isouter=True)
            .join(Item, UserItemLink.item_id == Item.id, isouter=True)
            .join(Task, User.id == Task.user_id, isouter=True)
            .offset(offset)
            .limit(limit)
            .where(User.tribe == user_tribe)
        ).all()

        return self._construct_user_views(user_with_items)

    async def update_user(self, user_id: UUID, user_update: UserUpdate) -> UserView:
        try:
            db_user = self.session.exec(select(User).where(User.id == user_id)).one()
            db_user_data = user_update.model_dump(exclude_unset=True)
            db_user.sqlmodel_update(db_user_data)
            self.session.add(db_user)
            self.session.commit()
            self.session.refresh(db_user)
            logger.info(f"Updated user: {db_user.username}")
            user_with_items = self.session.exec(
                select(User, UserItemLink, Item)
                .join(UserItemLink, User.id == UserItemLink.user_id, isouter=True)
                .join(Item, UserItemLink.item_id == Item.id, isouter=True)
                .where(User.id == db_user.id)
            ).all()
            return self._construct_user_view(user_with_items)
        except NoResultFound:
            raise UserNotFoundError(user_id=user_id)

    async def delete_user(self, user_id: UUID) -> None:
        try:
            db_user = self.session.exec(select(User).where(User.id == user_id)).one()
            self.session.delete(db_user)
            self.session.commit()
            logger.info(f"Deleted user: {db_user.username}")
        except NoResultFound:
            raise UserNotFoundError(user_id=user_id)

    async def update_user_password(self, user_id: UUID, password: str) -> UserView:
        try:
            db_user = self.session.exec(select(User).where(User.id == user_id)).one()
            db_user.password = password
            self.session.add(db_user)
            self.session.commit()
            self.session.refresh(db_user)
            logger.info(f"Updated user password: {db_user.username}")
            user_with_items = self.session.exec(
                select(User, UserItemLink, Item)
                .join(UserItemLink, User.id == UserItemLink.user_id, isouter=True)
                .join(Item, UserItemLink.item_id == Item.id, isouter=True)
                .where(User.id == db_user.id)
            ).all()
            return self._construct_user_view(user_with_items)
        except NoResultFound:
            raise UserNotFoundError(user_id=user_id)

    async def equip_item_to_user(
        self, user_id: UUID, item_id: UUID, equipped: bool
    ) -> UserView:
        try:
            self.session.exec(select(User).where(User.id == user_id)).one()
        except NoResultFound:
            raise UserNotFoundError(user_id=user_id)

        try:
            item_link = self.session.exec(
                select(UserItemLink).where(
                    UserItemLink.user_id == user_id, UserItemLink.item_id == item_id
                )
            ).one()
        except NoResultFound:
            raise ItemLinkToUserNotFoundError(item_id=item_id)

        item_link.equipped = equipped
        self.session.add(item_link)
        self.session.commit()
        self.session.refresh(item_link)

        return await self.get_user_by_id(user_id)

    async def get_user_by_id(self, user_id: UUID) -> UserView:
        user_with_items = self.session.exec(
            select(User, UserItemLink, Item)
            .join(UserItemLink, User.id == UserItemLink.user_id, isouter=True)
            .join(Item, UserItemLink.item_id == Item.id, isouter=True)
            .where(User.id == user_id)
        ).all()

        if not user_with_items:
            raise UserNotFoundError(user_id=user_id)

        return self._construct_user_view(user_with_items)

    def _construct_user_view(self, user_with_items) -> UserView:
        user, _, _ = user_with_items[0]

        user_items = [
            ItemUserView(
                **item.model_dump(),
                equipped=user_item_link.equipped,
            )
            for _, user_item_link, item in user_with_items
            if item
        ]

        return UserView(
            items=user_items,
            **user.model_dump(exclude={"password"}),
            tasks=[
                TaskView(
                    **task.model_dump(),
                )
                for task in user.tasks
            ],
        )

    def _construct_user_views(self, user_with_items) -> list[UserView]:
        users = {}
        for user, user_item_link, item, task in user_with_items:
            if user.id not in users:
                users[user.id] = {"user": user, "items": [], "tasks": []}
            if user_item_link and item:
                users[user.id]["items"].append(
                    ItemUserView(**item.model_dump(), equipped=user_item_link.equipped)
                )
            if task:
                if task.title not in [x.title for x in users[user.id]["tasks"]]:
                    users[user.id]["tasks"].append(TaskView(**task.model_dump()))

        return [
            UserView(
                **user_data["user"].model_dump(exclude={"password"}),
                items=user_data["items"],
                tasks=user_data["tasks"],
            )
            for user_data in users.values()
        ]
