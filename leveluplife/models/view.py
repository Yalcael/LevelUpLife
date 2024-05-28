from datetime import datetime
from uuid import UUID

from leveluplife.models.user import UserBase


class UserView(UserBase):
    id: UUID
    created_at: datetime
    strength: int = 5
    intelligence: int = 5
    agility: int = 5
    wise: int = 5
    psycho: int = 5
    experience: int = 0
