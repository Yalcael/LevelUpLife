from datetime import datetime
from uuid import UUID

from leveluplife.models.user import UserBase


class UserView(UserBase):
    id: UUID
    created_at: datetime
    strength: int = 0
    intelligence: int = 0
    agility: int = 0
    wise: int = 0
    psycho: int = 0
    experience: int = 0
