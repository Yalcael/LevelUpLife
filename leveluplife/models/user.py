from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlmodel import Field, AutoString

from leveluplife.models.shared import DBModel


class Tribe(str, Enum):
    NOSFERATI: str = "Nosferati"
    VALHARS: str = "Valhars"
    SAHARANS: str = "Saharans"
    GLIMMERKINS: str = "Glimmerkins"
    NEUTRALS: str = "Neutrals"

    @property
    def description(self) -> str:
        descriptions = {
            "Nosferati": "The Nosferati are a tribe of nocturnal beings who thrive in the shadows. Known for their agility and cunning, they possess a mysterious "
            "allure and a penchant for the dark arts. Their homeland is a gothic realm of eternal night, filled with ancient castles and dark forests.",
            "Valhars": "The Valhars are a tribe of mighty warriors and seafarers from the frozen north. They are renowned for their strength, bravery, and indomitable "
            "spirit. Living in a rugged landscape of snow-capped mountains and fjords, they honor their ancestors through epic sagas and battles.",
            "Saharans": "The Saharans hail from a vast desert land of golden sands and ancient cities. They are known for their intelligence, wisdom, and mastery of "
            "mystical arts. Their culture is rich with tales of legendary heroes, enchanted oases, and hidden treasures.",
            "Glimmerkins": "The Glimmerkins are a tribe of ingenious and whimsical beings who inhabit lush, enchanted forests and underground burrows. They are "
            "celebrated for their inventiveness, agility, and cheerful disposition. Their society thrives on creativity, clockwork inventions, "
            "and the magic of nature.",
            "Neutrals": "The Neutrals are those who have chosen not to align themselves with any particular tribe. They are versatile and independent individuals who "
            "prefer to forge their own path. While they do not possess the specific traits of the tribes, they benefit from a balanced set of attributes "
            "and the freedom to adapt to any situation.",
        }
        return descriptions[self.value]


class UserBase(DBModel):
    username: str = Field(default=None, index=True, min_length=3)
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)
    tribe: Tribe


class User(UserBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    strength: int = 0
    intelligence: int = 0
    agility: int = 0
    wise: int = 0
    psycho: int = 0
    experience: int = 0
    password: str = Field(min_length=4)


class UserCreate(UserBase):
    password: str


class UserUpdate(DBModel):
    username: Optional[str] | None = None
    email: Optional[EmailStr] | None = None
    strength: Optional[int] | None = None
    intelligence: Optional[int] | None = None
    agility: Optional[int] | None = None
    wise: Optional[int] | None = None
    psycho: Optional[int] | None = None
    experience: Optional[int] | None = None
    tribe: Optional[Tribe] | None = None


class UserUpdatePassword(DBModel):
    password: str
