from enum import Enum
from uuid import UUID

from sqlmodel import Field

from leveluplife.models.shared import DBModel


class ReactionType(str, Enum):
    LIKE: str = "like"
    DISLIKE: str = "dislike"
    SAD: str = "sad"
    HAPPY: str = "happy"
    CRAZY: str = "crazy"
    LAUGHING: str = "laughing"
    INLOVE: str = "inlove"
    DISAPPOINTING: str = "disappointing"

    @property
    def description(self) -> str:
        descriptions = {
            "like": "The user likes the task",
            "dislike": "The user dislikes the task",
            "sad": "The user is sad about the task",
            "happy": "The user is happy about the task",
            "crazy": "The user is crazy about the task",
            "laughing": "The user is laughing about the task",
            "inlove": "The user is in love with the task",
            "disappointing": "The user is disappointed about the task",
        }
        return descriptions[self.value]


class ReactionBase(DBModel):
    user_id: UUID | None = Field(foreign_key="user.id")
    task_id: UUID | None = Field(foreign_key="task.id")
    reaction: ReactionType


class ReactionCreate(ReactionBase):
    pass


class ReactionUpdate(DBModel):
    reaction: ReactionType | None = None
